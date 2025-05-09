# Hệ thống Monitoring với Prometheus, Grafana, Alertmanager và FastAPI

## 1. Yêu cầu hệ thống
- Docker & Docker Compose

## 2. Khởi động các dịch vụ giám sát (Prometheus, Grafana, Alertmanager...)

Tại thư mục `grafana/`, chạy lệnh sau:

```bash
cd grafana
sudo docker-compose up -d
```

Các dịch vụ sẽ chạy trên các cổng:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (user/pass mặc định: admin/admin)
- Pushgateway: http://localhost:9091
- Node Exporter: http://localhost:9100
- cAdvisor: http://localhost:8080
- Alertmanager: http://localhost:9093

## 3. Cấu hình thêm
- Sửa các file trong `grafana/prometheus/`, `grafana/alertmanager/` nếu muốn tùy chỉnh rule hoặc alert.

## 4. Dừng hệ thống

```bash
cd grafana
sudo docker-compose down
```

---
Mọi thắc mắc vui lòng liên hệ quản trị viên hệ thống. 