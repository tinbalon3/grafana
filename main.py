from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
instrumentator = Instrumentator()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + Prometheus"}

# expose metrics
instrumentator.instrument(app).expose(app)