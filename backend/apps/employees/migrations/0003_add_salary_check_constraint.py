from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0002_add_salary_min_validator"),
    ]

    operations = [
        # Remove any rows with invalid salary before adding the constraint
        migrations.RunSQL(
            sql="DELETE FROM employees WHERE salary < 1;",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.AddConstraint(
            model_name="employee",
            constraint=models.CheckConstraint(
                condition=models.Q(salary__gte=1),
                name="salary_min_1",
            ),
        ),
    ]
