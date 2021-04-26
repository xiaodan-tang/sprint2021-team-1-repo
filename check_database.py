import os
import django
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dinesafelysite.settings")
django.setup()

import django.apps  # noqa: E402
from user.models import UserActivityLog  # noqa: E402
from restaurant.models import Restaurant, AccessibilityRecord # noqa: E402

def count_records():
    total_count = 0
    for model in django.apps.apps.get_models():
        # name = model.__name__
        count = model.objects.all().count()
        total_count += count
        # print("{} rows: {}".format(name, count))

    return total_count

def reduce_activity_records():
    # Delete old user activity history
    time_threshold = datetime.now() - timedelta(days=10)
    UserActivityLog.objects.filter(last_visit__lt=time_threshold).delete()
    return count_records()

def reduce_accessibility_records():
    # delete accessibility record that doesn't match restaurant
    records = []
    for obj in Restaurant.objects.all():
        restaurant_street_number = obj.business_address.split()[0]
        q_result = (
            AccessibilityRecord.objects.filter(
                restaurant_name__iexact=obj.restaurant_name
            )
                .filter(street_number=restaurant_street_number)
                .first()
        )
        if q_result:
            records.append(q_result.id)

    candidates = []
    for obj in AccessibilityRecord.objects.all():
        if obj.id not in records:
            candidates.append(obj.id)

    for c in candidates:
        AccessibilityRecord.objects.filter(id=c).delete()

    return count_records()

if __name__ == "__main__":
    total_records = count_records()
    print("Check Database Start! Total Records: {}".format(total_records))
    if total_records > 10000:
        total_records = reduce_activity_records()
    if total_records > 10000:
        total_records = reduce_accessibility_records()
    print("Check Database Done! Total Records: {}".format(total_records))