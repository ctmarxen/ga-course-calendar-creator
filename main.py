from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime, date, timedelta
from workalendar.usa import UnitedStates

app = Flask(__name__)

day = datetime.now()

# Monday = 0 - 0
# Tuesday = 4.25 - 1
# Wednesday = 4.25 - 2
# Thursday = 2 - 3
# Friday = 0 - 4
# Saturday = 8 - 5
# Sunday = 0 - 6

cal = UnitedStates()

#need to add in choice of three day or four day
def course_calculator(month, day, year, type, hours=0):
    total_hours = 0
    course_dates = []
    holidays = []
    day_tracker = datetime(year, month, day)
    extra_holidays = [date(2021, 9, 4), date(2021, 11, 24), date(2021, 11, 27), date(2021, 12, 28), date(2021, 12, 29), date(2021, 12, 30), date(2022, 1, 15), date(2022, 2, 19)]
    while total_hours < 420:
        while type == 'three' and total_hours < 420:
            # can add holidays to this I believe, which could be stored in a database
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays):
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
            if not cal.is_holiday(date(day=day_tracker.day, month=day_tracker.month, year=day_tracker.year), extra_holidays=extra_holidays):
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
    return render_template("index.html")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
