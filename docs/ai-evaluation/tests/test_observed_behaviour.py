"""Reproduce observed limitations, not regression tests for corrected behaviour."""
from pathlib import Path
import hashlib
import importlib.util
import unittest
import pandas as pd

BASE = Path(__file__).resolve().parents[1]

def reviewed_module(name, expected_sha):
    path = BASE / 'evidence' / (name + '.py')
    data = path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    if actual != expected_sha:
        raise RuntimeError('Reviewed source snapshot changed: ' + name)
    spec = importlib.util.spec_from_file_location('reviewed_' + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

calc = reviewed_module('calculations', '51f688d00fc58781a5e30779ed64219fbbc4fef5')
health = reviewed_module('health', 'add676775fbeae3f621b884770c138f5945a1ab0')

class ObservedBehaviour(unittest.TestCase):
    def test_baseline_value(self):
        df = pd.DataFrame([{'Product':'A','Stock':10,'Price':2}])
        self.assertEqual(calc.calculate_inventory_value(df), 20)

    def test_duplicate_sales_inflate_value(self):
        inventory = pd.DataFrame([{'Product':'A','Stock':10,'Price':2}])
        sales = pd.DataFrame([{'Product':'A','DailySales':1},{'Product':'A','DailySales':2}])
        self.assertEqual(calc.calculate_inventory_value(inventory), 20)
        self.assertEqual(calc.calculate_inventory_value(inventory.merge(sales,on='Product')), 40)

    def test_missing_sales_drop_inventory(self):
        inventory = pd.DataFrame([{'Product':'A','Stock':10,'Price':2},{'Product':'B','Stock':5,'Price':4}])
        sales = pd.DataFrame([{'Product':'A','DailySales':1}])
        self.assertEqual(calc.calculate_inventory_value(inventory), 40)
        self.assertEqual(calc.calculate_inventory_value(inventory.merge(sales,on='Product')), 20)

    def test_zero_demand_uses_sentinel(self):
        df = pd.DataFrame([{'Stock':0,'DailySales':0}])
        value = calc.calculate_days_left(df).iloc[0]
        self.assertEqual(value, 999)
        self.assertTrue(value >= 21)  # Reconstructed app classification.

    def test_negative_sales_use_same_sentinel(self):
        df = pd.DataFrame([{'Stock':10,'DailySales':-1}])
        self.assertEqual(calc.calculate_days_left(df).iloc[0], 999)

    def test_rounding_crosses_boundary(self):
        df = pd.DataFrame([{'Stock':696,'DailySales':100}])
        self.assertLess(696/100, 7)
        self.assertEqual(calc.calculate_days_left(df).iloc[0], 7)

    def test_empty_population_is_critical(self):
        score = health.calculate_health_score(0,0,0)
        self.assertEqual(score, 0)
        self.assertIn('Critical', health.health_status(score))

if __name__ == '__main__':
    unittest.main()
