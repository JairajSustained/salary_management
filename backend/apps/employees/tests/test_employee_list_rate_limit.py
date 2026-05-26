import pytest
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.employees.models import RateLimitCounter

TEST_LIMIT = 3
TEST_WINDOW = 60


@pytest.fixture
def client():
	return APIClient()


@pytest.fixture(autouse=True)
def reset_rate_limit_state():
	cache.clear()
	RateLimitCounter.objects.all().delete()
	yield
	cache.clear()
	RateLimitCounter.objects.all().delete()


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_requests_under_limit_return_200(client):
	for _ in range(TEST_LIMIT):
		response = client.get(reverse("employee-list"))
		assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_request_exceeding_limit_returns_429(client):
	for _ in range(TEST_LIMIT):
		client.get(reverse("employee-list"))

	response = client.get(reverse("employee-list"))

	assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_429_response_contains_error_message(client):
	for _ in range(TEST_LIMIT):
		client.get(reverse("employee-list"))

	response = client.get(reverse("employee-list"))

	assert "error" in response.json()


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_retrieve_action_not_rate_limited(client, employee):
	# Fill the list counter past the limit
	for _ in range(TEST_LIMIT + 1):
		client.get(reverse("employee-list"))

	# Retrieve endpoint should be unaffected
	url = reverse("employee-detail", kwargs={"pk": employee.id})
	response = client.get(url)
	assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_create_action_not_rate_limited(client):
	# Fill the list counter past the limit
	for _ in range(TEST_LIMIT + 1):
		client.get(reverse("employee-list"))

	# POST to the same URL should not be rate limited
	response = client.post(reverse("employee-list"), {}, content_type="application/json")
	assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_db_backup_restores_count_on_cache_miss(client):
	"""When the file cache is cleared, the DB counter restores state so the rate limit holds."""
	# Make TEST_LIMIT - 1 requests to fill the counter partially
	for _ in range(TEST_LIMIT - 1):
		client.get(reverse("employee-list"))

	# Simulate cache file deletion
	cache.clear()

	# DB backup should restore count; this request brings us to exactly the limit
	response = client.get(reverse("employee-list"))
	assert response.status_code == status.HTTP_200_OK

	# One more request must be blocked
	response = client.get(reverse("employee-list"))
	assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
@override_settings(RATE_LIMIT=TEST_LIMIT, RATE_LIMIT_WINDOW=TEST_WINDOW)
def test_counter_increments_in_db_on_each_request(client):
	"""Every allowed request writes through to the DB backup."""
	for _ in range(TEST_LIMIT):
		client.get(reverse("employee-list"))

	counter = RateLimitCounter.objects.get(key="ratelimit:employee-list")
	assert counter.count == TEST_LIMIT
