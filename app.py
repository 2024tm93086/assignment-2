from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

workouts = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("workout", "").strip()
        duration = request.form.get("duration", "").strip()

        if name and duration.isdigit():
            workouts.append({"name": name, "duration": int(duration)})
            return redirect(url_for("workouts_page"))
        # if invalid, just fall through and re-render with a simple message
        return render_template("index.html", error="Enter a name and a numeric duration (minutes).")

    return render_template("index.html")


@app.route("/workouts")
def workouts_page():
    # total minutes, just to show something extra
    total = sum(w["duration"] for w in workouts)
    return render_template("workouts.html", workouts=workouts, total=total)
