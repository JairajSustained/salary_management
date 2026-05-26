from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone

CACHE_KEY = "ratelimit:employee-list"


class EmployeeListRateLimitMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_view(self, request, view_func, view_args, view_kwargs):
		if not self._is_employee_list(request, view_func):
			return None

		limit = int(settings.RATE_LIMIT)
		window = int(getattr(settings, "RATE_LIMIT_WINDOW", 60))

		count = self._get_count(window)

		if count >= limit:
			return JsonResponse(
				{"error": "Rate limit exceeded. Try again in a minute."},
				status=429,
			)

		self._increment(count, window)
		return None

	def _is_employee_list(self, request, view_func):
		from .views import EmployeeViewSet

		if not hasattr(view_func, "cls") or view_func.cls is not EmployeeViewSet:
			return False
		actions = getattr(view_func, "actions", {})
		return actions.get(request.method.lower()) == "list"

	def _get_count(self, window):
		"""Return current count, restoring from DB backup on cache miss."""
		count = cache.get(CACHE_KEY)
		if count is not None:
			return count
		return self._restore_from_db(window)

	def _restore_from_db(self, window):
		from .models import RateLimitCounter

		try:
			counter = RateLimitCounter.objects.get(key=CACHE_KEY)
		except RateLimitCounter.DoesNotExist:
			return 0

		now = timezone.now()
		elapsed = (now - counter.window_start).total_seconds()
		if elapsed >= window:
			# Window expired — treat as a fresh start
			return 0

		remaining_ttl = int(window - elapsed)
		cache.set(CACHE_KEY, counter.count, remaining_ttl)
		return counter.count

	def _increment(self, current_count, window):
		from .models import RateLimitCounter

		new_count = current_count + 1
		now = timezone.now()

		# Update cache
		cache.set(CACHE_KEY, new_count, window)

		# Write-through to DB backup
		counter, created = RateLimitCounter.objects.get_or_create(
			key=CACHE_KEY,
			defaults={"count": new_count, "window_start": now},
		)
		if not created:
			elapsed = (now - counter.window_start).total_seconds()
			if elapsed >= window:
				counter.window_start = now
				counter.count = new_count
			else:
				counter.count = new_count
			counter.save(update_fields=["count", "window_start"])
