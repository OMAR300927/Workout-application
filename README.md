# Workout Web App

A simple workout application for tracking workout programs.

This application has been deployed to a Kubernetes cluster using Minikube.

The application provides a table for creating and tracking workout programs.

---

## 🚀 Features

* Register and login
* Create workout programs
* Add images for workouts
* Update or delete workouts

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Frontend:** HTML, CSS
* **Database:** MongoDB

---

## ⚙️ Setup
1. Clone the repository

git clone https://github.com/OMAR300927/Workout-application.git
cd Workout-application

2. Install dependencies

This project uses uv with pyproject.toml

uv sync

✔ This will automatically:

- Create a .venv virtual environment
- Install all required dependencies

3. Create .env file

SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url

IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_URL=your_imagekit_url


4. Run the application

uv run main.py

---

## 📌 Notes

* Make sure the database is created in MongoDB Atlas.
* Ensure you have added your IP address to MongoDB Atlas before starting the app.
* I had some issues in the testing stage, so I added a secret file credential in Jenkins and used the .env file.

* For the secret file use the following command:
```
kubectl create secret generic app-secrets \
  --from-literal=MONGODB_INITDB_ROOT_USERNAME=your_db_username \
  --from-literal=MONGODB_INITDB_ROOT_PASSWORD=your_db_password \
  --from-literal=DATABASE_URL="mongodb+srv://your_db_username:your_db_password@mycluster.2yqqdvc.mongodb.net/?appName=your_cluster_name" \
  --from-literal=SECRET_KEY=your_secret_key \
  --from-literal=IMAGEKIT_PUBLIC_KEY="your_imagekit_public_key" \
  --from-literal=IMAGEKIT_PRIVATE_KEY="your_imagekit_private_key" \
  --from-literal=IMAGEKIT_URL="your_imagekit_url"
```

---

## 👨‍💻 Author

Omar Hussein
https://github.com/OMAR300927