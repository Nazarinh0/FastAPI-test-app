from fastapi import FastAPI


app = FastAPI(
    title="TestApp"
)


fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
]

@app.get("/")
def hello():
    return "Hello, World!"


@app.get("/users")
def get_all_users():
    return fake_users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]
