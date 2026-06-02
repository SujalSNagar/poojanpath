from datetime import timedelta

from django.utils import timezone


def get_delivery_dates():

    start_date = (
        timezone.now().date()
        + timedelta(days=7)
    )

    end_date = (
        timezone.now().date()
        + timedelta(days=10)
    )

    return start_date, end_date