from modules.schema import UserResponse, WorkoutResponse


def one_user(user):
    return UserResponse(
        id=str(user["_id"]),
        username=user.get("username"),
        email=user.get("email"),
        create_at=user.get("create_at")
    )


def all_users(users):
    return [one_user(user) for user in users]


def one_workout(workout):
    return WorkoutResponse(
        id=str(workout["_id"]),
        exercise_name=workout.get("exercise_name") or "",
        wights=workout.get("wights") or 0,
        sets=workout.get("sets") or 0,
        reps=workout.get("reps") or 0,
        rest_time=workout.get("rest_time") or 0,
        image=workout.get("image") or "",
        user_id=workout.get("user_id") or ""
    )


def all_workouts(workouts):
    return [one_workout(workout) for workout in workouts]