import unittest
import numpy as np
import pandas as pd
from scipy import stats

from src.data_loader import get_hourly_counts
from src.stats_engine import calculate_basic_stats, poisson_goodness_of_fit


class TestStatsPipeline(unittest.TestCase):
    def test_zero_filling_hourly_counts(self):
        # 2 events separated by 2 hours
        data = pd.DataFrame({
            'order_id': ['ORD-1', 'ORD-2'],
            'timestamp': pd.to_datetime(['2016-01-01 00:10:00', '2016-01-01 02:20:00']),
            'factory_id': ['Factory_Test', 'Factory_Test'],
            'quantity': [1, 2]
        })
        hourly = get_hourly_counts(data)
        self.assertEqual(len(hourly), 3)  # hours 00, 01, 02
        self.assertListEqual(list(hourly['order_count']), [1, 0, 1])

    def test_poisson_goodness_of_fit(self):
        np.random.seed(42)
        true_poisson = pd.Series(np.random.poisson(lam=10, size=5000))
        p_val_poisson = poisson_goodness_of_fit(true_poisson)
        self.assertGreater(p_val_poisson, 0.05)

        overdispersed = pd.Series(np.random.negative_binomial(n=5, p=0.3, size=5000))
        p_val_non = poisson_goodness_of_fit(overdispersed)
        self.assertLess(p_val_non, 0.05)

    def test_calculate_basic_stats(self):
        np.random.seed(42)
        dates = pd.date_range('2016-01-01', periods=100, freq='h')
        hourly_df = pd.DataFrame({
            'factory_id': ['Factory_A'] * 100,
            'timestamp': dates,
            'order_count': np.random.poisson(5, 100)
        })
        summary = calculate_basic_stats(hourly_df)
        self.assertEqual(len(summary), 1)
        self.assertIn('p_value_chi2', summary.columns)
        self.assertIn('dispersion_index', summary.columns)
        self.assertAlmostEqual(summary.iloc[0]['lambda_est'], 5.0, delta=0.5)


if __name__ == '__main__':
    unittest.main()
