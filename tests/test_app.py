def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Add a Workoust" in resp.data


def test_add_workout_success(client):
    resp = client.post("/add", data={
        "name": "Burpees",
        "duration": "10",
        "category": "Workout"
    }, follow_redirects=True)

    # Redirects to /workouts
    assert resp.status_code == 200
    assert b"Workout added!"


def test_category_grouping(client):
    client.post("/add", data={"name": "Neck Rolls",
                "duration": "3", "category": "Warmup"})
    client.post("/add", data={"name": "Pushups",
                "duration": "8", "category": "Workout"})
    client.post("/add", data={"name": "Stretch",
                "duration": "5", "category": "Cooldown"})

    resp = client.get("/workouts")
    body = resp.data

    assert b"Neck Rolls" in body
    assert b"Pushups" in body
    assert b"Stretch" in body


def test_validation_errors(client):
    r1 = client.post("/add", data={"name": "", "duration": "5",
                     "category": "Workout"}, follow_redirects=True)
    assert b"Please enter a workout name." in r1.data

    r2 = client.post("/add", data={"name": "Run", "duration": "xyz",
                     "category": "Workout"}, follow_redirects=True)
    assert b"Duration must be a positive number of minutes." in r2.data

    r3 = client.post("/add", data={"name": "Run", "duration": "0",
                     "category": "Workout"}, follow_redirects=True)
    assert b"Duration must be a positive number of minutes." in r3.data
