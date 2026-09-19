import os
import tempfile
import unittest

from app import create_app


class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = os.path.join(self.temp_dir.name, "test.sqlite3")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "DATABASE": self.database_path,
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_list_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("게시 대시보드".encode(), response.data)
        self.assertIn("아직 등록된 게시물이 없습니다.".encode(), response.data)

    def test_create_post_and_show_it_in_list(self):
        response = self.client.post(
            "/",
            data={"title": "서비스 점검 안내", "content": "금요일 오후 7시에 점검합니다."},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("게시물이 등록되었습니다.".encode(), response.data)
        self.assertIn("서비스 점검 안내".encode(), response.data)
        self.assertIn("금요일 오후 7시에 점검합니다.".encode(), response.data)

        with self.app.app_context():
            import sqlite3

            db = sqlite3.connect(self.database_path)
            count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
            db.close()

        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
