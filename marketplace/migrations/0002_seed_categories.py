from django.db import migrations


def create_categories(apps, schema_editor):
    Category = apps.get_model("marketplace", "Category")

    categories = [
        "Books",
        "Electronics",
        "Stationery",
        "Bicycles",
        "College Accessories",
        "Others",
    ]

    for category in categories:
        Category.objects.get_or_create(name=category)


def remove_categories(apps, schema_editor):
    Category = apps.get_model("marketplace", "Category")

    categories = [
        "Books",
        "Electronics",
        "Stationery",
        "Bicycles",
        "College Accessories",
        "Others",
    ]

    Category.objects.filter(name__in=categories).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_categories,
            remove_categories
        ),
    ]