import os
import time
import threading
import random
import socket

from fastapi import FastAPI
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, delete_from_gateway,REGISTRY,Histogram
from prometheus_fastapi_instrumentator import Instrumentator

# ----------------------------------------
# 🔧 Configuration từ biến môi trường
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://localhost:9091")
JOB_NAME = os.getenv("PUSHGATEWAY_JOB_NAME", "fastapi_app")
INSTANCE_ID = os.getenv("INSTANCE_ID", socket.gethostname())
PUSH_INTERVAL = int(os.getenv("METRICS_PUSH_INTERVAL", 10))
# ----------------------------------------


app = FastAPI(title="FastAPI + Prometheus + Pushgateway")

# 1️⃣ Đăng ký metric vào REGISTRY (default)
instrumentator = Instrumentator().instrument(app).expose(app)

# 2️⃣ Tạo registry mới và copy từ REGISTRY vào
push_registry = CollectorRegistry()

# 3️⃣ Copy toàn bộ collector từ REGISTRY sang push_registry
for collector in list(REGISTRY._collector_to_names.keys()):
    try:
        push_registry.register(collector)
    except ValueError:
        pass



# 📈 Metric tùy chỉnh
ONLINE_USERS = Gauge("online_users_total", "Số người đang online", registry=push_registry)
SESSIONS_IN = Gauge("user_sessions_in", "Số người mới vào", registry=push_registry)
SESSIONS_OUT = Gauge("user_sessions_out", "Số người vừa thoát", registry=push_registry)
AVERAGE_WEB_DURATION = Gauge("average_web_duration_seconds", "Thời gian ở lại trang web", registry=push_registry)
GPU_USAGE = Gauge("gpu_memory_utilization_percentage", "Mức sử dụng bộ nhớ GPU (%)", registry=push_registry)

# Nếu muốn đo thời gian xử lý thực sự của route (pull-based metric)
REQUEST_LATENCY = Histogram("web_request_duration_seconds", "Thời gian xử lý request", registry=REGISTRY)


print("[CHECK] Registered metric in push_registry:")
for c in push_registry._collector_to_names:
    print(c.__class__, c)

# 🔁 Vòng lặp push metric định kỳ
def push_metrics_loop():
    while True:
        try:
            # 🧪 Dữ liệu mô phỏng
            online = random.randint(10, 50)
            entered = random.randint(0, 5)
            left = random.randint(0, 3)
            web_time = random.uniform(5.0, 120.0)
            gpu = random.uniform(30.0, 90.0)

            ONLINE_USERS.set(online)
            SESSIONS_IN.set(entered)
            SESSIONS_OUT.set(left)
            AVERAGE_WEB_DURATION.set(web_time)
            GPU_USAGE.set(gpu)

            push_to_gateway(
                PUSHGATEWAY_URL,
                job=JOB_NAME,
                registry=push_registry,
                grouping_key={"instance": INSTANCE_ID}
            )

            print(f"[PUSH] Online={online} | In={entered} | Out={left} | WebTime={web_time:.1f}s | GPU={gpu:.1f}%")
        except Exception as e:
            print(f"[ERROR] Push failed: {e}")
        time.sleep(PUSH_INTERVAL)

# 🚀 Khởi động luồng push khi app start
@app.on_event("startup")
def start_pushing_metrics():
    threading.Thread(target=push_metrics_loop, daemon=True).start()

# 🧹 Xóa metric khi shutdown
@app.on_event("shutdown")
def cleanup_pushgateway_metrics():
    try:
        delete_from_gateway(
            PUSHGATEWAY_URL,
            job=JOB_NAME,
            grouping_key={"instance": INSTANCE_ID}
        )
        print(f"[SHUTDOWN] Metrics cleaned for instance {INSTANCE_ID}")
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {e}")

# 🌐 Route kiểm tra
@app.get("/")
def root():
    return {
        "message": "FastAPI with Pushgateway metrics",
        "instance": INSTANCE_ID
    }

@app.get("/simulate")
@REQUEST_LATENCY.time()  # Tự động đo thời gian chạy hàm này
def simulate_route():
    delay = random.uniform(0.1, 2.5)
    time.sleep(delay)
    return {"delay": delay}