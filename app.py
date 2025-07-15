import webbrowser
from datetime import datetime, timedelta

from flask import Flask, render_template, request

app = Flask(__name__)


# --- Homepage ---
@app.route("/")
def home():
    return render_template("index.html")


# --- Pregnancy Date Calculator ---
@app.route("/pregnancy-dates", methods=["GET", "POST"])
def pregnancy_dates():
    results = None
    error = None

    if request.method == "POST":
        try:
            transfer_date_str = request.form["transfer_date"]
            transfer_date = datetime.strptime(transfer_date_str, "%Y-%m-%d")
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
                "Calculated First Day of Last Menstrual Period (LMP)": format_date(lmp),
                "6.5 Week OB Ultrasound": format_date(obus_6w5d),
                "8.5 Week OB Ultrasound": format_date(obus_8w5d),
                "Week 10 (Last Day of Support Medications)": format_date(support_med_stop),
                "Week 20": format_date(week20),
                "Estimated Due Date (EDD)": format_date(edd),
            }

        except ValueError:
            error = "Invalid date format. Please enter date as MM/DD/YYYY."

    return render_template("pregnancy_dates.html", results=results, error=error)


# --- Embryo Transfer Chart Note Generator ---
@app.route("/transfer-note", methods=["GET", "POST"])
def transfer_note():
    note = None
    default_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    if request.method == "POST":
        date_str = request.form["transfer_date"]  # format: YYYY-MM-DD
        time_str = request.form["transfer_time"]  # format: HH:MM (24-hour)
        physician = request.form["physician"]

        try:
            # Parse date and time
            transfer_date = datetime.strptime(date_str, "%Y-%m-%d")
            transfer_time = datetime.strptime(time_str, "%H:%M")

            # Adjust to PM if entered in AM
            if transfer_time.hour < 12:
                transfer_time = transfer_time.replace(hour=transfer_time.hour + 12)

            # Format output values
            transfer_date_str = transfer_date.strftime("%m/%d/%Y")
            formatted_time = transfer_time.strftime("%-I:%M %p")
            check_in_time = (datetime.combine(transfer_date, transfer_time.time()) - timedelta(minutes=30)).strftime(
                "%-I:%M %p"
            )
            prog_start_date_str = (transfer_date - timedelta(days=5)).strftime("%m/%d/%Y")

            # Final note
            note = (
                f"Spoke with the patient regarding embryo transfer date and time. "
                f"Patient is scheduled for embryo transfer on {transfer_date_str} at {formatted_time} with {physician}. \n"
                f"Patient was instructed to check in at {check_in_time}, 30 minutes prior to transfer. \n"
                f"Patient was told to drink 1-1.5 L of water 1 hour prior to the procedure. \n"
                f"Progesterone injections will start on {prog_start_date_str} at {formatted_time}. "
                f"Instructions on progesterone administration were reviewed.\n"
                f"Patient was informed that one support person will be allowed in the transfer room. \n"
                f"Reminded patient (and support person if applicable) not to wear perfumes, fragranced products, or scented lotions. \n"
                f"An opportunity was given to ask questions regarding the embryo transfer and progesterone injections, and all questions were answered."
            )

        except ValueError:
            note = "Invalid input format. Please try again."

    return render_template("transfer_note.html", note=note, default_date=default_date)


if __name__ == "__main__":
    webbrowser.open("http://localhost:5050")
    app.run(debug=True, port=5050)
