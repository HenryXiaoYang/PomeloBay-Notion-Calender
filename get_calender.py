import calendar
from collections import defaultdict
from datetime import datetime

import aiohttp
from jinja2 import Template

from setting import NOTION_TOKEN, PROXY_URL


async def get_calendar(calendar_template):
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False), proxy=PROXY_URL) as session:
        all_data = []
        start_cursor = ""
        for _ in range(10):
            req_json = {"sorts": [{"property": "Date", "direction": "ascending"}]}
            if start_cursor:
                req_json["start_cursor"] = start_cursor

            async with session.post(
                    "https://api.notion.com/v1/databases/31b26a1b-d5da-4fbc-9741-068c2876cb10/query",
                    json=req_json
            ) as resp:
                data = await resp.json()
                all_data.extend(data.get("results", []))
                if not data.get("has_more"):
                    break
                start_cursor = data.get("next_cursor", "")

    # Process and clean data
    cleaned_data = []
    for item in all_data:
        # WHO EVER WROTE THE NOTION API IS GOD DAMN STUPID.
        date = item.get('properties', {}).get('Date', {}).get('date', {})
        if not date:  # Not valid
            continue
        date_str = date.get('start', None)  # Expected format: 'YYYY-MM-DD'
        if not date_str:  # Not valid
            continue
        name = item['properties']['Name']['title'][0]['plain_text']
        if name == '学年最后一天':
            pass
        students = [student['name'] for student in item['properties']['负责学生']['multi_select']]

        # Parse the date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        year_month = date_obj.strftime('%Y-%m')
        day = date_obj.day

        cleaned_data.append({
            'year_month': year_month,
            'day': day,
            'Name': name,
            'Students': students
        })

    # Group events by year_month and day
    grouped_events = defaultdict(lambda: defaultdict(list))
    for event in cleaned_data:
        ym = event['year_month']
        day = event['day']
        grouped_events[ym][day].append({
            'Name': event['Name'],
            'Students': event['Students']
        })

    # Prepare a sorted list of months
    sorted_year_months = sorted(grouped_events.keys())

    # For each month, get first_weekday and days_in_month, then organize into weeks
    months_data = []
    for ym in sorted_year_months:
        year, month = map(int, ym.split('-'))
        first_weekday, days_in_month = calendar.monthrange(year, month)  # first_weekday: Monday=0,...Sunday=6

        # Adjust first_weekday to make Sunday=0,...Saturday=6
        first_weekday = (first_weekday + 1) % 7

        # Generate a list of weeks, each week is a list of 7 days
        weeks = []
        week = []

        # Fill the first week with empty days if the month doesn't start on Sunday
        for _ in range(first_weekday):
            week.append(None)  # Represents an empty day

        current_day = 1
        while current_day <= days_in_month:
            week.append(current_day)
            if len(week) == 7:
                weeks.append(week)
                week = []
            current_day += 1

        # Fill the last week with empty days if necessary
        while len(week) < 7:
            week.append(None)
        if week:
            weeks.append(week)

        months_data.append({
            'year_month': ym,
            'weeks': weeks,
            'days_in_month': days_in_month,
            'events': grouped_events[ym]
        })

    # Render the template
    template = Template(calendar_template)
    html_content = template.render(months=months_data)

    return html_content

# asyncio.run(get_calender())
