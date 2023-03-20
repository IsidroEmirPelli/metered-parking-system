from django.utils import timezone


def discount_time_parked(parked, user_profile):
    """ Calculate the discount time """
    if parked.end_time is not None:
        end_time = parked.end_time.astimezone(timezone.utc).replace(tzinfo=None)
        start_time = parked.start_time.astimezone(timezone.utc).replace(tzinfo=None)
        time_parked = end_time - start_time
        hours_parked = time_parked.total_seconds() / 3600
        price = float(hours_parked) * float(user_profile.company.parking_price)
        return price
    Exception('The vehicle is still parked')

