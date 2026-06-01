from fastapi import APIRouter, Depends, HTTPException,status, File, UploadFile, Form
from fastapi.responses import RedirectResponse

from modules.schema import WorkoutUpdate
from modules.model import one_workout, all_workouts
from database import get_workout_collection
from auth.auth import get_current_user
from image import imagekit

from bson import ObjectId

router = APIRouter()


@router.get("/all-workouts")
def get_all_workouts(
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection)
):
    workouts = all_workouts(collection.find({"user_id": user_id}))

    return workouts


@router.get("/one-workout/{workout_id}")
def get_one_workout(
    workout_id: str,
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection)
):
    workout = collection.find_one({
        "_id": ObjectId(workout_id),
        "user_id": user_id
    })

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout doesn't exists"
        )
    
    return one_workout(workout)


@router.post("/add-workout", name="add_workout")
def add_workout(
    exercise_name: str = Form(...),
    wights: int = Form(0),
    sets: int = Form(...),
    reps: int = Form(...),
    rest_time: int = Form(0),
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection),
    file: UploadFile = File(...)
):
    exists_workout = collection.find_one({
        "exercise_name": exercise_name,
        "user_id": user_id
    })

    if exists_workout:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercise already exists"
        )
    
    try:
        image_url_value = None

        if file and file.filename:
            image_url = imagekit.files.upload(
                file=file.file,
                file_name=file.filename or "",
                tags=["Backend_upload"]
            )

            image_url_value = image_url.url

        new_workout = {
                "exercise_name": exercise_name,
                "wights": wights,
                "sets": sets,
                "reps": reps,
                "rest_time": rest_time,
                "image": image_url_value,
                "user_id": user_id
            }
        
        collection.insert_one(new_workout)

        return RedirectResponse(url="/", status_code=303)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.post("/update-workout/{workout_id}", name="update_workout")
def update_workout(
    workout_id: str,
    exercise_name: str = Form(...),
    wights: int = Form(0),
    sets: int = Form(...),
    reps: int = Form(...),
    rest_time: int = Form(0),
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection),
    file: UploadFile | None = File(None)
):
    get_workout = collection.find_one({
    "_id": ObjectId(workout_id),
    "user_id": user_id
})

    if not get_workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise doesn't exists"
        )
    
    workout = WorkoutUpdate(
        exercise_name=exercise_name,
        wights=wights,
        sets=sets,
        reps=reps,
        rest_time=rest_time,
    )
    
    updated_data = workout.model_dump(exclude_unset=True)

    if file and file.filename:
        image_url = imagekit.files.upload(
            file=file.file,
            file_name=file.filename or "",
            tags=["Backend_upload"]
        )

        updated_data["image"] = image_url.url

    collection.find_one_and_update(
        {
            "_id": ObjectId(workout_id),
            "user_id": user_id
        },
        {"$set": updated_data}
    )

    return RedirectResponse(url="/", status_code=303)


@router.post("/delete-workout/{workout_id}", name="delete_workout")
def delete_workout(
    workout_id: str,
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection)
):
    workout = collection.find_one_and_delete({
        "_id": ObjectId(workout_id),
        "user_id": user_id
    })

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise doesn't exists"
        )
    
    return RedirectResponse(url="/", status_code=303)