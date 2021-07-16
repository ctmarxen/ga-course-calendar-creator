from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, date, timedelta
from workalendar.usa import UnitedStates

app = Flask(__name__)

cal = UnitedStates()

course_dates = []
holidays = []
extra_holidays = [date(2021, 7, 3), date(2021, 9, 4), date(2021, 11, 24), date(2021, 11, 26), date(2021, 11, 27), date(2021, 12, 27), date(2021, 12, 28), date(2021, 12, 29), date(2021, 12, 30), date(2022, 1, 15), date(2022, 2, 19), date(2022, 5, 28), date(2022, 6, 17), date(2022, 6, 18), date(2022, 6, 19), date(2022, 7, 2), date(2022, 9, 3), date(2022, 11, 12), date(2022, 11, 23), date(2022, 11, 25), date(2022, 11, 26), date(2022, 12, 24), date(2022, 12, 27), date(2022, 12, 28), date(2022, 12, 29), date(2022, 12, 30), date(2022, 12, 31)]

holidays21 = []
holidays22 = []
day_tracker2 = datetime(2021, 7, 1)

while day_tracker2.year < 2023:
    if cal.is_holiday(date(day=day_tracker2.day, month=day_tracker2.month, year=day_tracker2.year), extra_holidays=extra_holidays) and cal.get_holiday_label(date(day=day_tracker2.day, month=day_tracker2.month, year=day_tracker2.year)) != 'Columbus Day':
        if day_tracker2.year == 2021:
            holidays21.append(day_tracker2.date().strftime("%m-%d-%Y"))
        else:
            holidays22.append(day_tracker2.date().strftime("%m-%d-%Y"))
    day_tracker2 += timedelta(days=1)

for _ in range(1,12):
    holidays21.append('')
print(len(holidays21))
print(len(holidays22))
#need to add in choice of three day or four day
def course_calculator(month, day, year, type, hours=0):
    total_hours = 0
    day_tracker = datetime(year, month, day)
    while total_hours < 420:
        while type == 'three' and total_hours < 420:
            # can add holidays to this I believe, which could be stored in a database
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays) or cal.get_holiday_label(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year)) == 'Columbus Day':
                # Tuesday
                if day_tracker.weekday() == 1:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Wednesday
                elif day_tracker.weekday() == 2:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Saturday
                elif day_tracker.weekday() == 5:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 8
            else:
                holidays.append(day_tracker.date().strftime("%m-%d-%Y"))
            # after adding hours, move forward a day
            day_tracker += timedelta(days=1)
            # Change weektype if the day is Sunday
            if day_tracker.weekday() == 6:
                type = "four"
        while type == 'four' and total_hours < 420:
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays) or cal.get_holiday_label(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year)) == 'Columbus Day':
                # Tuesday
                if day_tracker.weekday() == 1:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Wednesday
                elif day_tracker.weekday() == 2:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 4.25
                # Thursday
                elif day_tracker.weekday() == 3:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 2
                # Saturday
                elif day_tracker.weekday() == 5:
                    course_dates.append(day_tracker.date().strftime("%m-%d-%Y"))
                    total_hours += 8
            else:
                holidays.append(day_tracker.date().strftime("%m-%d-%Y"))
            # after adding hours, move forward a day
            day_tracker += timedelta(days=1)
            # Change weektype if the day is Sunday
            if day_tracker.weekday() == 6 and total_hours < 420:
                type = "three"
    # subtract one day to get the final day for the course
    day_tracker -= timedelta(days=1)
    print(len(course_dates))
    print(len(holidays))
    print(f"Total hours: {total_hours}")
    print(f"Final course day: {day_tracker.date().strftime('%m-%d-%Y')}")
    print(f"Course Dates: {course_dates}")
    print(f"Holidays: {holidays}")
    return {"hours": total_hours, "end": day_tracker.date().strftime('%m-%d-%Y'), 'dates': course_dates, 'holidays': holidays}

@app.route("/", methods=["GET","POST"])
def home():
    total_holidays = zip(holidays21, holidays22)
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
    return render_template("index.html", holidays=total_holidays)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
