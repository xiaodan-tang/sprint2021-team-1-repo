import os
import django
from restaurant.models import Restaurant
from restaurant.utils import get_latest_inspection_record

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()


def update_covid_compliant_status():
    restaurants = Restaurant.objects.all()
    for r in restaurants:
        compliant_status = get_latest_inspection_record(
            business_name=r.restaurant_name,
            business_address=r.business_address,
            postcode=r.postcode,
        )["is_roadway_compliant"]
        r.compliant_status = compliant_status
        r.save()


if __name__ == "__main__":
    update_covid_compliant_status()
