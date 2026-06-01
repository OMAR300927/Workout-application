
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException as authException

from database import get_workout_collection
from modules.model import all_workouts, one_workout
from auth.auth import get_current_user
from routes import users, workout

from bson import ObjectId


app = FastAPI(
    title="Workout application",
    description="This is were you can add your workout program"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router=users.router, prefix="/api/users", tags=["users"])
app.include_router(router=workout.router, prefix="/api/workouts", tags=["workouts"])


@app.get("/register", include_in_schema=False)
def register(request: Request):
    return templates.TemplateResponse(
        request,
        "Register.html"
    )
    

@app.get("/login", include_in_schema=False)
def login(request: Request):
    return templates.TemplateResponse(
        request,
        "Login.html"
    )


@app.get("/", include_in_schema=False)
def home(
    request: Request,
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection)
):
    workouts = all_workouts(collection.find({"user_id": user_id}))

    return templates.TemplateResponse(
        request,
        "Home.html",
        context={
            "workouts": workouts
        }
    )


@app.get("/update-page/{workout_id}")
def update_page(
    request: Request,
    workout_id: str,
    user_id: str = Depends(get_current_user),
    collection = Depends(get_workout_collection)
):
    workout = one_workout(collection.find_one({
        "_id": ObjectId(workout_id),
        "user_id": user_id
    }))

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )

    return templates.TemplateResponse(
        request,
        "update_workout.html",
        context={
            "workout": workout
        }
    )


@app.exception_handler(authException)
def authentication(request: Request, exc: authException):
    if exc.status_code == 401:
        return RedirectResponse("/login", status_code=303)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc)}
    )