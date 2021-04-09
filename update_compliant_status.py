import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from restaurant.models import Restaurant, InspectionRecords  # noqa: E402


def update_covid_compliant_status():
    restaurants = Restaurant.objects.all()
    for r in restaurants:
        inspection_records = InspectionRecords.objects.filter(
            restaurant_name=r.restaurant_name,
            business_address=r.business_address,
            postcode=r.postcode,
        ).order_by("-inspected_on")

        if len(inspection_records) >= 1:
            latest_compliant_status = inspection_records[0].is_roadway_compliant
            r.compliant_status = latest_compliant_status
            r.save()


if __name__ == "__main__":
    update_covid_compliant_status()
