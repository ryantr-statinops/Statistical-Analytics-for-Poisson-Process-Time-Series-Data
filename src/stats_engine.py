import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime

def calculate_basic_stats(hourly_df):
    """
    Tính toán các chỉ số thống kê đặc trưng cho từng nhà máy.
    """
    stats_list = []
    
    # Chia nhóm theo từng nhà máy để phân tích riêng biệt
    for factory, group in hourly_df.groupby('factory_id'):
        counts = group['order_count']
        
        mean_val = counts.mean()      # Kỳ vọng E[N(t)]
        var_val = counts.var()        # Phương sai Var[N(t)]
        std_val = counts.std()        # Độ lệch chuẩn
        
        # Chỉ số phân tán (Index of Dispersion) - Nếu ~ 1 thì là Poisson chuẩn
        iod = var_val / mean_val if mean_val != 0 else 0

        # Kiểm định Chi-square mức độ phù hợp với phân phối Poisson
        p_val = poisson_goodness_of_fit(counts)

        stats_list.append({
            'factory_id': factory,
            'lambda_est': round(mean_val, 3),
            'variance': round(var_val, 3),
            'dispersion_index': round(iod, 3),
            'p_value_chi2': round(p_val, 4) if pd.notna(p_val) else None,
            'max_orders_hr': counts.max(),
            'total_sample_hours': len(counts)
        })
    
    return pd.DataFrame(stats_list)

def poisson_goodness_of_fit(group_data, min_expected=5):
    """
    Kiểm định xem dữ liệu có thực sự tuân theo phân phối Poisson không.
    Sử dụng kiểm định Chi-square với ddof=1 (do lambda ước lượng từ dữ liệu)
    và gom nhóm (bin pooling) các tần suất kỳ vọng nhỏ hơn min_expected.
    """
    if len(group_data) == 0:
        return np.nan
    mu = float(group_data.mean())
    if mu <= 0:
        return np.nan

    n = len(group_data)
    max_k = int(group_data.max())
    k_vals = np.arange(0, max(max_k + 1, int(mu + 4 * np.sqrt(mu)) + 1))

    obs_series = group_data.value_counts()
    f_obs_raw = np.array([obs_series.get(k, 0) for k in k_vals], dtype=float)
    if group_data.max() > k_vals[-1]:
        f_obs_raw[-1] += (group_data > k_vals[-1]).sum()

    f_exp_raw = stats.poisson.pmf(k_vals, mu) * n
    f_exp_raw[-1] = stats.poisson.sf(k_vals[-1] - 1, mu) * n
    f_exp_raw = f_exp_raw * (n / f_exp_raw.sum())

    f_obs_pooled = []
    f_exp_pooled = []
    cur_obs = 0.0
    cur_exp = 0.0
    for obs, exp in zip(f_obs_raw, f_exp_raw):
        cur_obs += obs
        cur_exp += exp
        if cur_exp >= min_expected:
            f_obs_pooled.append(cur_obs)
            f_exp_pooled.append(cur_exp)
            cur_obs = 0.0
            cur_exp = 0.0

    if cur_exp > 0:
        if len(f_exp_pooled) > 0:
            f_obs_pooled[-1] += cur_obs
            f_exp_pooled[-1] += cur_exp
        else:
            f_obs_pooled.append(cur_obs)
            f_exp_pooled.append(cur_exp)

    f_obs = np.array(f_obs_pooled)
    f_exp = np.array(f_exp_pooled)
    f_exp = f_exp * (f_obs.sum() / f_exp.sum())

    ddof = 1
    if len(f_obs) <= ddof + 1:
        return np.nan

    chi2, p_val = stats.chisquare(f_obs=f_obs, f_exp=f_exp, ddof=ddof)
    return float(p_val)

def _format_markdown_table(df):
    try:
        return df.to_markdown(index=False)
    except (ImportError, ModuleNotFoundError):
        headers = [str(c) for c in df.columns]
        header_row = "| " + " | ".join(headers) + " |"
        sep_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        data_rows = [
            "| " + " | ".join(str(val) for val in row) + " |"
            for row in df.values
        ]
        return "\n".join([header_row, sep_row] + data_rows)

def export_report(summary_df, file_name='data/processed/final_report.md'):
    """Tạo báo cáo dưới dạng file Markdown để lưu trữ"""
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("# BÁO CÁO PHÂN TÍCH QUÁ TRÌNH NGẪU NHIÊN (SOFA)\n\n")
        f.write(f"Ngày ghi nhận dữ liệu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 1. Bảng tóm tắt chỉ số các nhà máy\n\n")
        f.write(_format_markdown_table(summary_df))
        f.write("\n\n## 2. Nhận xét thống kê\n\n")

        for _, row in summary_df.iterrows():
            f.write(f"### Nhà máy: {row['factory_id']}\n")
            f.write(f"- Tốc độ đơn hàng trung bình (lambda): {row['lambda_est']} đơn/giờ.\n")
            f.write(f"- Phương sai: {row['variance']} | Chỉ số phân tán (Dispersion Index): {row['dispersion_index']}.\n")

            p_val = row.get('p_value_chi2')
            if p_val is not None and pd.notna(p_val):
                f.write(f"- Kiểm định Chi-square Poisson (p-value): {p_val}\n")
                if p_val > 0.05:
                    f.write("  - Đánh giá kiểm định: Không bác bỏ giả định Poisson (dữ liệu phù hợp với phân phối Poisson ở mức ý nghĩa 5%).\n")
                else:
                    f.write("  - Đánh giá kiểm định: Bác bỏ giả định Poisson (dữ liệu có sự sai lệch đáng kể so với phân phối Poisson).\n")

            if 0.9 <= row['dispersion_index'] <= 1.1:
                f.write("- Đánh giá phân tán: Hoạt động chuẩn theo phân phối Poisson (Equidispersion).\n\n")
            elif row['dispersion_index'] > 1.1:
                f.write("- Đánh giá phân tán: Có dấu hiệu biến động bất thường cao hơn kỳ vọng (Overdispersion).\n\n")
            else:
                f.write("- Đánh giá phân tán: Biến động thấp hơn kỳ vọng (Underdispersion).\n\n")
    print(f"--- Đã xuất báo cáo chuyên sâu tại {file_name} ---")