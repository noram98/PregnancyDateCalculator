import webbrowser
from datetime import datetime, timedelta

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    print("Request received:", request.method)
    results = None
    error = None

    if request.method == "POST":
        try:
            transfer_date_str = request.form["transfer_date"]
            transfer_date = datetime.strptime(transfer_date_str, "%m/%d/%Y")

            lmp = transfer_date - timedelta(days=19)
            obus_6w5d = lmp + timedelta(weeks=6, days=5)
            obus_8w5d = lmp + timedelta(weeks=8, days=5)
            support_med_stop = lmp + timedelta(weeks=10)
            week20 = lmp + timedelta(weeks=20)
            edd = lmp + timedelta(weeks=40)

            def format_date(date):
                return date.strftime("%m/%d/%Y")

            results = {
                "Embryo Transfer Date": format_date(transfer_date),
                "Calculated LMP": format_date(lmp),
                "6w5d OBUS": format_date(obus_6w5d),
                "8w5d OBUS": format_date(obus_8w5d),
                "Week 10 (Last Day of Support Medications)": format_date(support_med_stop),
                "Week 20": format_date(week20),
                "Estimated Due Date (EDD)": format_date(edd),
            }

        except ValueError:
            error = "Invalid date format. Please enter date as MM/DD/YYYY."

    return render_template("form.html", results=results, error=error)


if __name__ == "__main__":
    webbrowser.open("http://localhost:5050")
    app.run(debug=True, port=5050)
