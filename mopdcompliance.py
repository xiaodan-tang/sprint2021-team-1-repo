import os
import django
from restaurant.models import Restaurant

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()


def populate_mopd_compliance_status():
    restaurants = Restaurant.objects.all()
    for r in restaurants:
        compliant = r.is_accessible_compliant()
        if compliant:
            r.mopd_compliance_status = "Compliant"
        else:
            r.mopd_compliance_status = "Non-Compliant"
        r.save()


if __name__ == "__main__":
    populate_mopd_compliance_status()
