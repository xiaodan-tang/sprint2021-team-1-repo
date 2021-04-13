import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from restaurant.models import Restaurant, AccessibilityRecord, FAQ  # noqa: E402


def insert_static_mopd_data():
    with open("static/2019_accessibility_compliance.csv") as f:
        reader = csv.reader(f)
        is_header = True
        for row in reader:
            if is_header:
                is_header = False
                continue
            try:
                obj, created = AccessibilityRecord.objects.get_or_create(
                    restaurant_name=row[0],
                    compliant=row[1],
                    business_address=row[2],
                    street_number=row[3],
                    street_name=row[4],
                    city=row[5],
                    postcode=row[6],
                )
            except Exception:
                continue


def populate_mopd_compliance_status():
    restaurants = Restaurant.objects.all()
    for r in restaurants:
        compliant = r.is_accessible_compliant()
        if compliant:
            r.mopd_compliance_status = "Compliant"
        else:
            r.mopd_compliance_status = "Non-Compliant"
        r.save()


def insert_static_faq_data():
    with open("static/FAQs.csv") as f:
        reader = csv.reader(f)
        is_header = True
        for row in reader:
            if is_header:
                is_header = False
                continue
            try:
                obj, created = FAQ.objects.get_or_create(question=row[0], answer=row[1])
            except Exception:
                continue


if __name__ == "__main__":
    insert_static_mopd_data()
    populate_mopd_compliance_status()
    insert_static_faq_data()
