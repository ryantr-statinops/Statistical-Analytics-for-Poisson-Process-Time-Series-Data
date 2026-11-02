# BÁO CÁO PHÂN TÍCH QUÁ TRÌNH NGẪU NHIÊN (SOFA)

Ngày ghi nhận dữ liệu: 2026-11-02 11:46:17

## 1. Bảng tóm tắt chỉ số các nhà máy

| factory_id | lambda_est | variance | dispersion_index | p_value_chi2 | max_orders_hr | total_sample_hours |
| --- | --- | --- | --- | --- | --- | --- |
| Factory_A | 5.019 | 5.04 | 1.004 | 0.464 | 16 | 26304 |
| Factory_B | 11.975 | 12.018 | 1.004 | 0.2559 | 29 | 26304 |
| Factory_C | 30.001 | 29.856 | 0.995 | 0.7133 | 55 | 26304 |

## 2. Nhận xét thống kê

### Nhà máy: Factory_A
- Tốc độ đơn hàng trung bình (lambda): 5.019 đơn/giờ.
- Phương sai: 5.04 | Chỉ số phân tán (Dispersion Index): 1.004.
- Kiểm định Chi-square Poisson (p-value): 0.464
  - Đánh giá kiểm định: Không bác bỏ giả định Poisson (dữ liệu phù hợp với phân phối Poisson ở mức ý nghĩa 5%).
- Đánh giá phân tán: Hoạt động chuẩn theo phân phối Poisson (Equidispersion).

### Nhà máy: Factory_B
- Tốc độ đơn hàng trung bình (lambda): 11.975 đơn/giờ.
- Phương sai: 12.018 | Chỉ số phân tán (Dispersion Index): 1.004.
- Kiểm định Chi-square Poisson (p-value): 0.2559
  - Đánh giá kiểm định: Không bác bỏ giả định Poisson (dữ liệu phù hợp với phân phối Poisson ở mức ý nghĩa 5%).
- Đánh giá phân tán: Hoạt động chuẩn theo phân phối Poisson (Equidispersion).

### Nhà máy: Factory_C
- Tốc độ đơn hàng trung bình (lambda): 30.001 đơn/giờ.
- Phương sai: 29.856 | Chỉ số phân tán (Dispersion Index): 0.995.
- Kiểm định Chi-square Poisson (p-value): 0.7133
  - Đánh giá kiểm định: Không bác bỏ giả định Poisson (dữ liệu phù hợp với phân phối Poisson ở mức ý nghĩa 5%).
- Đánh giá phân tán: Hoạt động chuẩn theo phân phối Poisson (Equidispersion).

