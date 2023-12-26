from fastapi import FastAPI


app = FastAPI(
    title="TestApp"
)

@app.get("/")
def hello():
    return "Hello, World!"
