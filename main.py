import os
import matplotlib.pyplot as plt

# Import các module từ thư mục src
from src.data_loader import factory_data_loader, get_hourly_counts
from src.stats_engine import calculate_basic_stats, export_report
from src.visualizer import plot_order_trends, plot_distribution_comparison
if __name__ == "__main__":
    # BƯỚC 1: Tải dữ liệu từ data/raw/
    # Chúng ta lọc từ năm 2016 đến 2018 như mục tiêu dự án
    print("--- Đang bắt đầu quá trình tải dữ liệu ---")
    raw_data = factory_data_loader(start_year=2016, end_year=2018)
    
    # Kiểm tra nếu tải dữ liệu thành công thì mới làm các bước tiếp theo
    if raw_data is not None:
        # BƯỚC 2: Gom nhóm theo giờ (Aggregation)
        hourly_data = get_hourly_counts(raw_data)
        
        # BƯỚC 3: Phân tích thống kê
        print("\n" + "="*50)
        print("KẾT QUẢ PHÂN TÍCH QUÁ TRÌNH NGẪU NHIÊN")
        print("="*50)
        
        summary_stats = calculate_basic_stats(hourly_data)
        print(summary_stats.to_string(index=False))
        
        # BƯỚC 4: Xuất báo cáo và Trực quan hóa
        os.makedirs('data/processed', exist_ok=True)
        
        # Xuất file báo cáo Markdown
        export_report(summary_stats)
        
        # Vẽ biểu đồ xu hướng
        print("\n--- Đang vẽ biểu đồ xu hướng... ---")
        plot_order_trends(hourly_data)

        
        # Vẽ biểu đồ so sánh phân phối cho các Factory (để kiểm chứng Poisson)
        fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
        plot_distribution_comparison(hourly_data, "Factory_A", ax=axs[0])
        plot_distribution_comparison(hourly_data, "Factory_B", ax=axs[1])
        plot_distribution_comparison(hourly_data, "Factory_C", ax=axs[2])

        axs[0].set_ylabel('Mật độ (Density)')
        axs[1].set_ylabel('')
        axs[2].set_ylabel('')

        axs[0].set_xlabel('Số đơn hàng / Giờ')
        axs[1].set_xlabel('Số đơn hàng / Giờ')
        axs[2].set_xlabel('Số đơn hàng / Giờ')

        plt.tight_layout()
        plt.show()
    else:
        print("Lỗi: Không có dữ liệu để xử lý. Vui lòng kiểm tra lại thư mục data/raw/")