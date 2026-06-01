from fastapi import status

from bson import ObjectId


# get all workouts
def test_get_all_workouts(logged_in_client):
    workouts = logged_in_client.get(
        "/api/workouts/all-workouts"
    )

    assert workouts.status_code == status.HTTP_200_OK


# get one workout
def test_get_one_workout(logged_in_client, test_db):
    add_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-1",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert add_workout.status_code == 303
    assert add_workout.headers["location"] == "/"

    workout = test_db["test_workouts"].find_one({"exercise_name": "exercise-1"})

    workout_id = str(workout["_id"])

    get_workout = logged_in_client.get(
        f"/api/workouts/one-workout/{workout_id}"
    )

    assert get_workout.status_code == status.HTTP_200_OK
    assert get_workout.json()["exercise_name"] == "exercise-1"


# get one workout error
def test_get_workout_invalid(logged_in_client):
    fake_id = str(ObjectId())

    get_workout = logged_in_client.get(
        f"/api/workouts/one-workout/{fake_id}"
    )

    assert get_workout.status_code == status.HTTP_404_NOT_FOUND


# add workout
def test_add_workout(logged_in_client):
    add_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-2",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert add_workout.status_code == 303
    assert add_workout.headers["location"] == "/"


# add workout error
def test_add_workout_duplicated(logged_in_client):
    add_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-3",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert add_workout.status_code == 303
    assert add_workout.headers["location"] == "/"

    exists_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-3",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert exists_workout.status_code == status.HTTP_400_BAD_REQUEST


# update workout
def test_update_workout(logged_in_client, test_db):
    add_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-4",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert add_workout.status_code == 303
    assert add_workout.headers["location"] == "/"

    workout = test_db["test_workouts"].find_one({"exercise_name": "exercise-4"})

    workout_id = str(workout["_id"])

    update_workout = logged_in_client.post(
        f"/api/workouts/update-workout/{workout_id}",
        data={
            "exercise_name": "exercise-4",
            "wights": 50,
            "sets": 10,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert update_workout.status_code == 303
    assert update_workout.headers["location"] == "/"


# delete workout
def test_delete_workout(logged_in_client, test_db):
    add_workout = logged_in_client.post(
        "/api/workouts/add-workout",
        data={
            "exercise_name": "exercise-5",
            "wights": 50,
            "sets": 3,
            "reps": 10,
            "rest_time": 60,
        },
        files={
            "file": ("test.png", b"fake image", "image/png")
        },
        follow_redirects=False 
    )

    assert add_workout.status_code == 303
    assert add_workout.headers["location"] == "/"

    workout = test_db["test_workouts"].find_one({"exercise_name": "exercise-5"})

    workout_id = str(workout["_id"])

    delete_workout = logged_in_client.post(
        f"/api/workouts/delete-workout/{workout_id}",
        follow_redirects=False
    )

    assert delete_workout.status_code == 303
    assert delete_workout.headers["location"] == "/"