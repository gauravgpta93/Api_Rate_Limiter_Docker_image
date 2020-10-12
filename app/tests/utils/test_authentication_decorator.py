import unittest

from app.main.index import app


class TestDecorator(unittest.TestCase):

    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self) -> None:
        pass

    def test_correct_header(self):
        """
        Checks the response in case of correct headers
        :return:
        """
        response = self.app.get("/limit", headers={"X-API-KEY": "test_0"})
        self.assertEqual(response.status_code, 200)

    def test_wrong_header(self):
        """
        Checks if the no header is provided and in case of missing correct header
        :return:
        """
        response = self.app.get("/limit")
        self.assertEqual(response.status_code, 401)
        response = self.app.get("/limit", headers={"X-API-KEY1": "test_0"})
        self.assertEqual(response.status_code, 401)
