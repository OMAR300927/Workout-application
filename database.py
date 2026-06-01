from pymongo import MongoClient

from config import settings


uri = settings.database_url

client = MongoClient(uri)

db = client.workout_app

users_collection = db["users"]

workout_collection = db["workouts"]

def get_db():
    return db

def get_users_collection():
    return users_collection

def get_workout_collection():
    return workout_collection