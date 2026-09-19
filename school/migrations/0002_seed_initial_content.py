from django.db import migrations


CATEGORIES = [
    ("elementary", "Základní škola", "🏫", "elementary", "Kapitola první", "Místo pro zvídavost, přátelství a první velké objevy. Naše škola provází děti od prvního kroku až k samostatnému přemýšlení.", [("aktuality", "Aktuality"), ("zaci", "Pro žáky"), ("rodice", "Pro rodiče")]),
    ("kindergarten", "Mateřská škola", "🧒", "kindergarten", "Kapitola druhá", "Svět prvních kamarádství, her a objevování. Každý den přináší malé dobrodružství.", [("den", "Náš den"), ("nejmensi", "Pro nejmenší"), ("zapis", "Zápis do školky")]),
    ("canteen", "Školní jídelna", "🍎", "canteen", "Kapitola třetí", "Dobré jídlo, energie na celý den a přehledný jídelníček pro každého.", [("jidelnicek", "Jídelníček"), ("alergeny", "Alergeny"), ("platby", "Platby obědů")]),
    ("club", "Školní družina", "🧸", "club", "Kapitola čtvrtá", "Odpoledne plná her, tvoření, pohybu a času stráveného společně.", [("aktivity", "Co podnikáme"), ("krouzky", "Kroužky"), ("rodice", "Pro rodiče")]),
]


def seed_content(apps, schema_editor):
    Category = apps.get_model("school", "Category")
    Subcategory = apps.get_model("school", "Subcategory")
    for order, (slug, name, icon, theme_class, chapter, lead, links) in enumerate(CATEGORIES):
        category = Category.objects.create(slug=slug, name=name, icon=icon, theme_class=theme_class, chapter=chapter, lead=lead, sort_order=order)
        for sub_order, (sub_slug, sub_name) in enumerate(links):
            Subcategory.objects.create(category=category, slug=sub_slug, name=sub_name, sort_order=sub_order)


def remove_content(apps, schema_editor):
    apps.get_model("school", "Category").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("school", "0001_initial")]
    operations = [migrations.RunPython(seed_content, remove_content)]
