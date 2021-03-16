import string
import random
from django.utils import timezone




def id_generator(size=6):
    chars=string.ascii_uppercase + string.digits
    uid = ''.join(random.choice(chars) for _ in range(size))
    return uid


def get_current_datetime(date_only=False):
    current_time = timezone.now()
    if date_only: current_time = current_time.date()
    return current_time