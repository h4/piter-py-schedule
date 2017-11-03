import datetime
import requests
from icalendar import Calendar, Event

from lxml import html


def parse_time(time_str):
    try:
        return datetime.time(*map(int, time_str.replace('.', ':').split(':')))
    except:
        return datetime.time()


def get_ts(col, date):
    times = "".join(col.itertext()).strip().replace('\xa0', ' ').split(' - ')
    return [datetime.datetime.combine(date, parse_time(t)) for t in times]


def process_row(cal, date, row):
    cols = row.findall('td')
    begin, end = get_ts(cols[0], date)
    if len(cols) == 2:
        event = Event()
        event.add('dtstart', begin)
        event.add('dtend', end)
        event.add('summary', "".join(cols[1].itertext()).strip())
        cal.add_component(event)
    else:
        for col in cols[1:]:
            event = Event()
            event.add('dtstart', begin)
            event.add('dtend', end)
            first_link = col.find('.//a')
            if first_link is not None:
                event.add('summary', "".join(first_link.itertext()).strip())
                cal.add_component(event)


def generate():
    url = 'https://it-events.com/events/8527/program'
    req = requests.get(url)
    data = req.text

    cal = Calendar()
    date = datetime.date(2017, 11, 2)

    tree = html.fromstring(data)
    for row in tree.body.findall('.//tr'):
        first_col = "".join(row.find('td').itertext()).strip()
        if first_col.startswith('День'):
            day = date.day
            date = date.replace(day=day + 1)
            continue
        if first_col.startswith('Время'):
            continue
        if len(first_col) == 0:
            continue
        process_row(cal, date, row)
    return cal.to_ical()


if __name__ == '__main__':
    generate()
