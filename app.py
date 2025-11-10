from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret"

workouts = []


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    duration = request.form.get("duration", "").strip()
    category = request.form.get("category", "Workout")

    # basic validation
    if not name:
        flash("Please enter a workout name.")
        return redirect(url_for("index"))

    try:
        minutes = int(duration)
        if minutes <= 0:
            raise ValueError()
    except ValueError:
        flash("Duration must be a positive number of minutes.")
        return redirect(url_for("index"))

    if category not in ["Warmup", "Workout", "Cooldown"]:
        category = "Workout"

    workouts.append({"name": name, "duration": minutes, "category": category})
    flash("Workout added!")
    return redirect(url_for("index"))


@app.route("/workouts", methods=["GET"])
def list_workouts():
    grouped = {"Warmup": [], "Workout": [], "Cooldown": []}
    for w in workouts:
        grouped[w["category"]].append(w)
    return render_template("workouts.html", grouped=grouped)
