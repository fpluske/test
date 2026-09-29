from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("school", "0002_seed_initial_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("image", models.ImageField(upload_to="home_photos/")),
                ("title", models.CharField(blank=True, max_length=160)),
                ("alt_text", models.CharField(blank=True, max_length=160)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "fotografie na úvodní stránce",
                "verbose_name_plural": "fotografie na úvodní stránce",
                "ordering": ["sort_order", "-created_at"],
            },
        ),
    ]
