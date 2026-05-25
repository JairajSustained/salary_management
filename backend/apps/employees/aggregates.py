from django.db.models import Aggregate, DecimalField


class Median(Aggregate):
    """PostgreSQL PERCENTILE_CONT(0.5) ordered-set aggregate for computing median salary."""

    function = "PERCENTILE_CONT"
    name = "Median"
    template = "%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)"
    output_field = DecimalField()
    allow_distinct = False
