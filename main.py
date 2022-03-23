from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, date, timedelta
from workalendar.usa import UnitedStates

app = Flask(__name__)

cal = UnitedStates()

extra_holidays = [date(2021, 7, 3), date(2021, 9, 4), date(2021, 11, 24), date(2021, 11, 26), date(2021, 11, 27), date(2021, 12, 27), date(2021, 12, 28), date(2021, 12, 29), date(2021, 12, 30), date(2022, 1, 15), date(2022, 2, 19), date(2022, 5, 28), date(2022, 6, 18), date(2022, 6, 19), date(2022, 7, 2), date(2022, 9, 3), date(2022, 11, 12), date(2022, 11, 23), date(2022, 11, 25), date(2022, 11, 26), date(2022, 12, 24), date(2022, 12, 27), date(2022, 12, 28), date(2022, 12, 29), date(2022, 12, 30), date(2022, 12, 31), date(2023, 1, 2), date(2023, 1, 14), date(2023, 1, 16), date(2023, 2, 18), date(2023, 2, 20), date(2023, 5, 27), date(2023, 5, 29), date(2023, 6, 17), date(2023, 6, 19), date(2023, 7, 1), date(2023, 7, 4), date(2023, 9, 2), date(2023, 9, 4), date(2023, 11, 10), date(2023, 11, 11), date(2023, 11, 22), date(2023, 11, 23), date(2023, 11, 24), date(2023, 11, 25), date(2023, 12, 23), date(2023, 12, 25), date(2023, 12, 26), date(2023, 12, 27), date(2023, 12, 28), date(2023, 12, 29), date(2023, 12, 30), date(2024, 1, 1)]

holidays22 = []
holidays23 = []
day_tracker2 = datetime(2022, 1, 1)

while day_tracker2.year < 2024:
    if cal.is_holiday(date(day=day_tracker2.day, month=day_tracker2.month, year=day_tracker2.year), extra_holidays=extra_holidays) and cal.get_holiday_label(date(day=day_tracker2.day, month=day_tracker2.month, year=day_tracker2.year)) != 'Columbus Day':
        if day_tracker2.year == 2022:
            holidays22.append(day_tracker2.date().strftime("%m-%d-%Y"))
        else:
            holidays23.append(day_tracker2.date().strftime("%m-%d-%Y"))
    day_tracker2 += timedelta(days=1)

for _ in range(1,11):
    holidays22.append('')
print(len(holidays22))
print(len(holidays23))

#need to add in choice of three day or four day
def course_calculator(month, day, year, type):
    holidays = []
    course_dates = []
    dates_by_week = []
    total_hours = 0
    day_tracker = datetime(year, month, day)
    week_dates = []
    if type == 'three' or type == 'four':
        hour_goal = 420
    else:
        hour_goal = 480
    while total_hours < hour_goal:
        while type == 'three' and total_hours < hour_goal:
            # can add holidays to this I believe, which could be stored in a database
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays) or cal.get_holiday_label(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year)) == 'Columbus Day':
                # Tuesday
                if day_tracker.weekday() == 1:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Wednesday
                elif day_tracker.weekday() == 2:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Saturday
                elif day_tracker.weekday() == 5:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 8
            else:
                if day_tracker.weekday() in [1, 2, 5]:
                    holidays.append(day_tracker.date().strftime("%m-%d-%Y"))
            # after adding hours, move forward a day
            day_tracker += timedelta(days=1)
            # Change weektype if the day is Sunday
            if day_tracker.weekday() == 6:
                if week_dates != []:
                    dates_by_week.append(week_dates)
                    week_dates = []
                type = "four"
            if total_hours >= hour_goal:
                dates_by_week.append(week_dates)
        while type == 'four' and total_hours < hour_goal:
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays) or cal.get_holiday_label(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year)) == 'Columbus Day':
                # Tuesday
                if day_tracker.weekday() == 1:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Wednesday
                elif day_tracker.weekday() == 2:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Thursday
                elif day_tracker.weekday() == 3:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 2
                # Saturday
                elif day_tracker.weekday() == 5:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 8
            else:
                if day_tracker.weekday() in [1, 2, 3, 5]:
                    holidays.append(day_tracker.date().strftime("%m-%d-%Y"))
            # after adding hours, move forward a day
            day_tracker += timedelta(days=1)
            # Change weektype if the day is Sunday
            if day_tracker.weekday() == 6:
                if week_dates != []:
                    dates_by_week.append(week_dates)
                    week_dates = []
                type = "three"
            if total_hours >= hour_goal:
                dates_by_week.append(week_dates)
        while type == 'noalt' and total_hours < hour_goal:
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays) or cal.get_holiday_label(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year)) == 'Columbus Day':
                # Tuesday
                if day_tracker.weekday() == 1:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Wednesday
                elif day_tracker.weekday() == 2:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Thursday
                elif day_tracker.weekday() == 3:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 3.5
                # Saturday
                elif day_tracker.weekday() == 5:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    week_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 8
            else:
                if day_tracker.weekday() in [1, 2, 3, 5]:
                    holidays.append(day_tracker.date().strftime("%m-%d-%Y"))
            # after adding hours, move forward a day
            day_tracker += timedelta(days=1)
            if day_tracker.weekday() == 6:
                if week_dates != []:
                    dates_by_week.append(week_dates)
                    week_dates = []
            if total_hours >= hour_goal:
                dates_by_week.append(week_dates)
    # subtract one day to get the final day for the course
    day_tracker -= timedelta(days=1)
    print(len(course_dates))
    print(len(holidays))
    print(f"Total hours: {total_hours}")
    print(f"Final course day: {day_tracker.date().strftime('%m-%d-%Y')}")
    print(f"Course Dates: {course_dates}")
    print(f"Holidays: {holidays}")
    print(dates_by_week)
    return {"hours": total_hours, "end": day_tracker.date().strftime('%m-%d-%Y'), 'weeks': dates_by_week, 'holidays': holidays}

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        first_week = request.form.get("first-week")
        print(first_week)
        start_date = request.form.get("start-date")
        divided_date = start_date.split("-")
        print(divided_date)
        year = int(divided_date[0])
        month = int(divided_date[1])
        day = int(divided_date[2])
        data = course_calculator(year=year, month=month, day=day, type=first_week)
        return render_template("result.html", data=data, start=start_date)
    return render_template("index.html", holidays=zip(holidays22, holidays23))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
