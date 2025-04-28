# Grafana + Prometheus + FastAPI Monitoring

## Mô tả
Dự án này thiết lập hệ thống giám sát ứng dụng FastAPI bằng **Prometheus**, **Pushgateway**, và **Grafana**.
FastAPI đẩy các chỉ số (metrics) về Pushgateway, từ đó Prometheus thu thập và Grafana hiển thị trực quan.

## Cấu trúc dự án
```
grafana/
├── docker-compose.yml
├── main.py
├── prometheus.yml
└── grafana/
    └── dashboards/ (chứa dashboard JSON)
```

- **docker-compose.yml**: Khởi động Grafana, Prometheus, Pushgateway.
- **prometheus.yml**: Cấu hình scrape từ Pushgateway.
- **main.py**: FastAPI đẩy metrics về Pushgateway.

## Thành phần
- **FastAPI**: Ứng dụng backend push metrics.
- **Prometheus**: Thu thập metrics.
- **Pushgateway**: Nhận metrics trung gian.
- **Grafana**: Hiển thị dashboards.

## Hướng dẫn chạy
### 1. Khởi động hệ thống
```bash
docker-compose up -d
```
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Pushgateway: `http://localhost:9091`

### 2. Cài đặt Grafana
- Đăng nhập: `admin/admin`
- Add datasource: **Prometheus** với URL `http://prometheus:9090`
- Import dashboard từ file JSON (nếu có).

### 3. Chạy FastAPI
```bash
pip install fastapi uvicorn prometheus_client
uvicorn main:app --reload
```

### 4. Gửi metrics
Gới endpoint FastAPI để push metrics lên Pushgateway.

## Metrics hiển thị trên dashboard
| Metric | Ý nghĩa |
|:---|:---|
| online_users_total | Số người dùng online |
| user_sessions_in | Lượt vào hệ thống |
| user_sessions_out | Lượt rời khỏi hệ thống |
| http_request_duration_seconds | Độ trễ trung bình |
| http_requests_total | Số lượng requests/giây (RPS) |
| http_request_duration_seconds_bucket | P50/P95/P99 độ trễ |
| gpu_memory_utilization_percentage | Tỷ lệ dùng RAM GPU |
| average_web_duration_seconds | Thời gian trung bình trên web |
| http_request_duration_seconds_ask | Thời gian xử lý request web giả lập |

## Ghi chú
- Dashboard đã thiết lập sẵn nhiều metric quan trọng.
- Có thể tự tạo alert rule ở Prometheus theo nhu cầu.

## Tài liệu tham khảo
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

