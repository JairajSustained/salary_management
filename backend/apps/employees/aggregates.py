from django.db.models import Aggregate, DecimalField


class Median(Aggregate):
	function = "PERCENTILE_CONT"
	name = "Median"
	template = "%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)"
	output_field = DecimalField()
	allow_distinct = False
