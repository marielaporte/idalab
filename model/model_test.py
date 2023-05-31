import unittest
import numpy as np
from model import ICUZen


class TestICUZen(unittest.TestCase):

    def test_init(self):
        model = ICUZen()
        self.assertEqual(model.threshold, 0.76)
        self.assertEqual(model.sensitivity, 30)

    def test_predict_proba(self):
        model = ICUZen()
        X = np.array([[37, 120, 80, 90, 18]])
        scores = model.predict_proba(X)
        self.assertTrue(0 <= scores <= 1)

    def test_predict(self):
        model = ICUZen()
        X = np.array([[37, 120, 80, 90, 18]])
        alarms = model.predict(X)
        self.assertTrue(alarms.any())

    def test_alarm_thresholds(self):
        # Raise temperature threshold
        model = ICUZen()
        X = np.array([[38, 120, 80, 90, 18]])  # Higher temperature
        alarms = model.predict(X)
        self.assertTrue(alarms.any())
        print(alarms)

        # Lower systolic pressure threshold
        model = ICUZen()
        X = np.array([[37, 115, 80, 90, 18]])  # Lower systolic pressure
        alarms = model.predict(X)
        self.assertTrue(alarms.any())

        # Raise diastolic pressure threshold
        model = ICUZen()
        X = np.array([[37, 120, 85, 90, 18]])  # Higher diastolic pressure
        alarms = model.predict(X)
        self.assertTrue(alarms.any())

        # Raise heart rate threshold
        model = ICUZen()
        X = np.array([[37, 120, 80, 95, 18]])  # Higher heart rate
        alarms = model.predict(X)
        print(alarms)
        self.assertTrue(alarms.any())


        # Raise respiratory rate threshold
        model = ICUZen()
        X = np.array([[37, 120, 80, 90, 20]])  # Higher respiratory rate
        alarms = model.predict(X)
        self.assertTrue(alarms.any())

    def test_normal_vitals(self):
        model = ICUZen()

        normal_vitals = np.array([[
            37,  # Normal temperature
            120,  # Normal systolic pressure
            80,  # Normal diastolic pressure
            80,  # Normal heart rate
            18  # Normal respiratory rate
        ]])

        alarms = model.predict(normal_vitals)

        self.assertFalse(alarms.any())


if __name__ == '__main__':
    unittest.main()