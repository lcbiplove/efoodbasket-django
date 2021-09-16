import datetime
import calendar
from django import template

DAYS = list(calendar.day_name)


register = template.Library()


@register.filter
def get_this_week_by_day(day: str):
    today = datetime.date.today()
    current_day = today.weekday()
    day_num = DAYS.index(day.capitalize())
    remainder = day_num - current_day
    date_time = today + datetime.timedelta(days=remainder)
    return date_time

@register.filter
def get_next_week_by_day(day: str):
    date_time = get_this_week_by_day(day)
    return date_time + datetime.timedelta(days=7)