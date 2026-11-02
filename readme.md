
# Statistical Analytics for Poisson Process Time Series Data

## 1. Tổng quan dự án

**Mục tiêu:** sử dụng các phương pháp thống kê để mô tả và phân tích dữ liệu dòng đơn hàng theo **Poisson process** (quá trình ngẫu nhiên), từ đó trực quan hóa sự khác biệt về số đơn theo thời gian và giữa các nhà máy.

**Bối cảnh:** hệ thống gồm **n nhà máy** (mặc định `n = 3`). Số lượng và tham số sinh dữ liệu có thể tinh chỉnh tại `data_gen.py`. Mục tiêu là mô hình hóa việc xuất hiện ngẫu nhiên của đơn hàng theo **đơn/giờ**, sau đó so sánh sự khác biệt giữa các nhà máy với số  **đơn/giờ** khác nhau dựa trên thống kê của chuỗi thời gian.


---

## 2. Các thành phần trọng tâm

### A. Data Modeling (Thiết kế dữ liệu)

Thay vì sử dụng các dữ liệu mẫu có sẵn, dự án xây dựng `data_gen.py` để tự động tạo dữ liệu cho các nhà máy nhằm tối ưu hiệu suất và tăng tính linh động khi người dùng muốn kiểm tra sự khác nhau giữa các bộ dữ liệu tương đồng nhưng có số lượng/đặc tính khác nhau.


* **Dữ liệu nguồn:** 3 file CSV riêng biệt cho 3 nhà máy (Factory A, B, C).
* **Biến số chính:** `timestamp` (thời điểm đơn hàng đến), `order_id`, và `factory_id`.
* **Logic:** Chuyển đổi dữ liệu từ dạng "Sự kiện rời rạc" (Discrete Events) sang dạng "Tần suất theo khung giờ" (Hourly Aggregation) để phục vụ mô hình hóa.

### B. Statistics (Thống kê chuyên sâu)

Các phương pháp phân tích trong dự án sử dụng gồm:

* **Aggregation theo giờ (hourly aggregation):** Gom dữ liệu sự kiện rời rạc theo từng khung giờ để thu được chuỗi thời gian `order_count` cho mỗi `factory_id`.
* **Tính toán các chỉ số thống kê cơ bản theo factory:** Tính **mean (ước lượng λ)**, **variance**, **std** của số đơn/giờ.
* **Chỉ số phân tán (dispersion index):**
  - `dispersion_index = variance / mean`
  - Nếu gần **1** ⇒ phù hợp với giả định **Poisson**; nếu khác nhiều ⇒ có thể **overdispersion**.
* **Kiểm định phù hợp phân phối Poisson (Poisson goodness-of-fit):**
  - Dùng **Chi-square** với `ddof=1` (ước lượng tham số $\lambda$) và gom cụm bin nhỏ (bin pooling) để so sánh tần suất quan sát với tần suất kỳ vọng.
  - `p_value_chi2 > 0.05`: Chưa có bằng chứng bác bỏ giả định Poisson (dữ liệu tuân theo Poisson).
* **Trực quan hóa:**
  - **Rolling mean (trung bình trượt 24h)** để quan sát xu hướng dòng đơn theo thời gian.
  - **Histogram so sánh phân phối** cho từng nhà máy, kết hợp vẽ đè hàm khối xác suất lý thuyết (**Poisson PMF stem plot**) để đối chiếu trực quan.

### C. Vận hành & Kỹ thuật

* **Tech Stack:**
  - **Python**: điều phối pipeline chạy toàn bộ quá trình tạo dữ liệu → nạp dữ liệu → thống kê → trực quan hóa.
  - **pandas**: đọc/ghép CSV, xử lý `timestamp`, group theo thời gian (hourly aggregation).
  - **numpy**: sinh dữ liệu giả lập theo phân phối **Poisson** trong `data_gen.py` và hỗ trợ tính toán.
  - **scipy**: thực hiện kiểm định thống kê (Poisson goodness-of-fit bằng **Chi-square**).
  - **matplotlib** + **seaborn**: vẽ biểu đồ xu hướng và histogram so sánh phân phối trong `src/visualizer.py`.

* **Cấu trúc module:** Phân tách mã nguồn thành các file/chức năng riêng biệt:
  - `data_gen.py`: tạo dữ liệu giả lập (Poisson events) và ghi ra `data/raw/*.csv`.
  - `src/data_loader.py`: tải CSV, lọc theo khoảng năm, sau đó chuyển sang dạng theo giờ (`order_count`).
  - `src/stats_engine.py`: tính thống kê (mean/variance/std, dispersion index) và xuất báo cáo Markdown.
  - `src/visualizer.py`: vẽ rolling mean và histogram phân phối.

* **Tính linh hoạt:** Hệ thống cho phép tùy chọn khoảng thời gian phân tích (ví dụ: 2016-2018), tinh chỉnh tham số `lam` (thay đổi tốc độ đơn/giờ) và so sánh nhiều nhà máy thông qua cấu hình chạy ở `main.py`.


Code ví dụ:

```python
generate_factory_data(factory_name="name", lam=x)
```

Trong đó:
- `factory_name` (str): tên nhà máy.
- `x` / `lam` (float): **tốc độ trung bình** λ = số đơn hàng kỳ vọng **trong 1 giờ**.

Ghi chú:
- `lam` là tham số điều khiển cường độ của quá trình Poisson (tạo số đơn/giờ từ phân phối Poisson).
- Dữ liệu sinh ra là các **sự kiện rời rạc theo thời gian** (`timestamp`) và sau đó được **gom theo giờ** để phân tích chuỗi `order_count`.

---


## 3. Cấu trúc thư mục dự án

Dự án chia cấu trúc thư mục phân biệt theo từng chức năng để dễ dàng mở rộng và tái sử dụng cho trường hợp khác:

```plaintext
project_stochastic/
|
├── data/              # Chứa dữ liệu thô và dữ liệu sau tính toán
|   ├── raw/           # Chứa 3 file CSV dữ liệu gốc của các nhà máy
|   └── processed/     # Dữ liệu trung gian sau tiền xử lý
|   
├── result/            # Chứa các báo cáo kết quả đầu ra
|   └── final_report.md# Báo cáo tổng hợp thống kê & kiểm định Poisson
|
├── src/               # Chứa các Module tính toán chuyên biệt
|   ├── data_loader.py # Module đọc file và zero-fill chuỗi thời gian theo giờ
|   ├── stats_engine.py# Module tính chỉ số thống kê & kiểm định Chi-square Poisson
|   └── visualizer.py  # Module vẽ đồ thị xu hướng và so sánh phân phối thực tế vs lý thuyết
|
├── tests/             # Bộ kiểm thử đơn vị & kiểm định thống kê
|   └── test_stats_pipeline.py
|
├── main.py            # Script thực thi chính điều phối toàn bộ pipeline
├── data_gen.py        # Script khởi tạo dữ liệu giả lập Poisson ban đầu
└── requirements.txt   # Danh sách thư viện phụ thuộc
```
---

## 4. Hướng dẫn triển khai (Step-by-Step)

1. **Bước 1:** Kích hoạt môi trường ảo tại terminal:
   ```bash
   .venv\Scripts\Activate.ps1
   ```
2. **Bước 2:** Chạy `data_gen.py` để tạo dữ liệu giả lập Poisson cho giai đoạn 2016 - 2018:
   ```bash
   python data_gen.py
   ```
3. **Bước 3:** (Tùy chọn) Chạy kiểm thử tự động để xác nhận tính toàn vẹn của pipeline:
   ```bash
   python -m unittest discover tests
   ```
4. **Bước 4:** Chạy `main.py` để thực thi toàn bộ luồng phân tích và hiển thị trực quan hóa:
   ```bash
   python main.py
   ```
5. **Bước 5:** Xem kết quả phân tích thống kê và kiểm định Poisson chi tiết tại `result/final_report.md`.

---
