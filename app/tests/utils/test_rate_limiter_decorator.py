import unittest
import time
from app.main.index import app


class TestDecorator(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self) -> None:
        pass

    def test_slow_rate(self):
        """
        Test for within the rate
        :return:
        """
        for i in range(10):
            response = self.app.get("/limit", headers={"X-API-KEY": "test_1"})
            self.assertEqual(response.status_code, 200)
        time.sleep(2)
        for i in range(10):
            response = self.app.get("/limit", headers={"X-API-KEY": "test_1"})
            self.assertEqual(response.status_code, 200)

    def test_excess_rate(self):
        """
        Test for exceeding the rate
        :return:
        """
        for i in range(10):
            response = self.app.get("/limit", headers={"X-API-KEY": "test_2"})
            self.assertEqual(response.status_code, 200)
        response = self.app.get("/limit", headers={"X-API-KEY": "test_2"})
        self.assertEqual(response.status_code, 429)

    def test_different_id(self):
        """
        Test with different User ID
        :return:
        """
        for i in range(10):
            response = self.app.get("/limit", headers={"X-API-KEY": "test_3"})
            self.assertEqual(response.status_code, 200)
            response = self.app.get("/limit", headers={"X-API-KEY": "test_4"})
            self.assertEqual(response.status_code, 200)
        response = self.app.get("/limit", headers={"X-API-KEY": "test_3"})
        self.assertEqual(response.status_code, 429)
        response = self.app.get("/limit", headers={"X-API-KEY": "test_4"})
        self.assertEqual(response.status_code, 429)