import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson
import numpy as np

def plot_order_trends(hourly_df):
    """Vẽ biểu đồ xu hướng đơn hàng theo thời gian cho các nhà máy"""
    plt.figure(figsize=(15, 6))
    for factory in hourly_df['factory_id'].unique():
        subset = hourly_df[hourly_df['factory_id'] == factory]
        # Vẽ trung bình trượt (Rolling Mean) để bớt nhiễu và thấy xu hướng
        plt.plot(subset['timestamp'], subset['order_count'].rolling(window=24).mean(), label=factory)
    
    plt.title('Xu hướng đơn hàng trung bình (Rolling 24h) - 2016-2018')
    plt.xlabel('Thời gian')
    plt.ylabel('Số đơn hàng / Giờ')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_distribution_comparison(hourly_df, factory_name, ax=None):
    
    subset = hourly_df[hourly_df['factory_id'] == factory_name]['order_count']
    if subset.empty:
        return

    mu = subset.mean()

    if ax is None:
        ax = plt.gca()

    # Vẽ Histogram quan sát vào ô ax
    sns.histplot(subset, binwidth=1, stat="density", color='skyblue', alpha=0.6, label='Quan sát thực tế', ax=ax)

    # Vẽ Poisson lý thuyết vào ô ax
    x = np.arange(0, int(subset.max()) + 1)
    markerline, stemlines, baseline = ax.stem(
        x, poisson.pmf(x, mu),
        linefmt='tab:red',
        markerfmt='r.',
        basefmt=" ",
        label=f'Poisson lý thuyết (λ={mu:.2f})'
    )
    plt.setp(markerline, markersize=5)
    plt.setp(stemlines, linewidth=1.2, alpha=0.8)

    ax.set_title(f'Phân phối {factory_name}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Số đơn hàng / Giờ')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', frameon=True)
