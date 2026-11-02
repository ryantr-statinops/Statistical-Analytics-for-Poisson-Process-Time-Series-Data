import pandas as pd
import numpy as np
import os
import datetime as dt


def setup_folders():
    # Danh sách các thư mục cần thiết cho dự án
    folders = ['data/raw', 'data/processed']
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"--- Đã tạo thư mục: {folder} ---")

def generate_factory_data(factory_name, lam, start_year=2016, end_year=2018):
    date_range = pd.date_range(start =f'{start_year}-01-01', end = f'{end_year}-12-31 23:00:00', freq = 'h')

    orders_count = np.random.poisson(lam, len(date_range))

    data = []
    for i, dt in enumerate(date_range):
        n_orders = orders_count[i]
        for _ in range(n_orders):
            random_minute = np.random.randint(0, 60)
            random_second = np.random.randint(0, 60)
            order_time = dt.replace(minute=random_minute, second=random_second)
            
            data.append({
                'order_id': f"ORD-{order_time.strftime('%y%m%d%H%M%S')}-{np.random.randint(10,99)}",
                'timestamp': order_time,
                'factory_id': factory_name,
                'quantity': np.random.randint(1, 10) # Quy mô đơn hàng
            })
            
    df = pd.DataFrame(data)
    file_path = f'data/raw/{factory_name}_orders.csv'
    df.to_csv(file_path, index=False)
    print(f"--- Đã tạo xong dữ liệu cho {factory_name} tại {file_path} ---")

# THỰC THI: Tạo 3 nhà máy với đặc tính thống kê khác nhau
if __name__ == "__main__":
    setup_folders()
    # Factory A: Ổn định (5 đơn/giờ)
    generate_factory_data("Factory_A", lam=5)

    # Factory B: Bận rộn hơn (12 đơn/giờ)
    generate_factory_data("Factory_B", lam=12)

    # Factory C: Có sự biến động (Non-stationary - giả lập bằng cách tăng lambda lên)
    generate_factory_data("Factory_C", lam=30)