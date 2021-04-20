import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

from restaurant.models import Restaurant, InspectionRecords  # noqa: E402


def delete_old_records():
    all_restaurants = Restaurant.objects.all()
    for r in all_restaurants:
        inspection_recs = InspectionRecords.objects.filter(business_id=r.business_id)
        newest_rec = inspection_recs[0]
        for i in inspection_recs:
            if i.inspected_on >= newest_rec.inspected_on:
                newest_rec = i
        for i in inspection_recs:
            if i != newest_rec:
                try:
                    i.delete()
                except Exception:
                    continue


if __name__ == "__main__":
    delete_old_records()
