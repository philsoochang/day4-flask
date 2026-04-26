import os
import sqlite3
import sys
import tempfile
import unittest


class PostListPaginationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.db_path = os.path.join(cls.temp_dir.name, "test_board.db")
        os.environ["DB_PATH"] = cls.db_path

        if "app" in sys.modules:
            del sys.modules["app"]

        import app as app_module

        cls.app_module = app_module
        cls.client = app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        os.environ.pop("DB_PATH", None)
        cls.temp_dir.cleanup()

    def setUp(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM posts")
        rows = []
        for i in range(1, 26):
            rows.append(
                (
                    f"테스트 글 {i}",
                    f"테스트 본문 {i}",
                    None,
                    f"2026-01-{i:02d} 12:00:00",
                )
            )
        for i in range(1, 16):
            rows.append(
                (
                    f"파이썬 검색 제목 {i}",
                    f"검색 전용 내용 {i}",
                    None,
                    f"2026-02-{i:02d} 12:00:00",
                )
            )
        rows.append(
            (
                "일반 제목",
                "이 본문에는 키워드 파이썬이 포함됩니다",
                None,
                "2026-03-01 12:00:00",
            )
        )
        rows.append(("가나다 테스트", "정렬 확인", None, "2025-12-01 12:00:00"))
        rows.append(("나다라 테스트", "정렬 확인", None, "2025-12-02 12:00:00"))
        rows.append(("다라마 테스트", "정렬 확인", None, "2025-12-03 12:00:00"))
        conn.executemany(
            "INSERT INTO posts (title, content, image, created_at) VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.commit()
        conn.close()

    def test_first_page_shows_10_posts_and_disables_prev(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("일반 제목", html)
        self.assertIn("파이썬 검색 제목 15", html)
        self.assertNotIn("파이썬 검색 제목 6", html)
        self.assertIn("1 / 5", html)
        self.assertIn('id="first-page" aria-disabled="true"', html)
        self.assertIn('id="prev-page" aria-disabled="true"', html)
        self.assertIn('id="next-page" aria-disabled="false"', html)
        self.assertIn('id="last-page" aria-disabled="false"', html)
        self.assertIn('id="list-header-date"', html)
        self.assertIn('id="list-header-title"', html)
        self.assertIn('id="list-header-content"', html)
        self.assertIn('id="search-input"', html)
        self.assertIn('id="search-button"', html)

    def test_middle_page_shows_10_posts_and_enables_both_buttons(self):
        response = self.client.get("/?page=2")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("파이썬 검색 제목 6", html)
        self.assertIn("테스트 글 22", html)
        self.assertNotIn("파이썬 검색 제목 7", html)
        self.assertNotIn("테스트 글 21", html)
        self.assertIn("2 / 5", html)
        self.assertIn('id="first-page" aria-disabled="false"', html)
        self.assertIn('id="prev-page" aria-disabled="false"', html)
        self.assertIn('id="next-page" aria-disabled="false"', html)
        self.assertIn('id="last-page" aria-disabled="false"', html)

    def test_last_page_disables_next_button(self):
        response = self.client.get("/?page=5")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("테스트 글 1", html)
        self.assertNotIn("테스트 글 2", html)
        self.assertIn("5 / 5", html)
        self.assertIn('id="first-page" aria-disabled="false"', html)
        self.assertIn('id="prev-page" aria-disabled="false"', html)
        self.assertIn('id="next-page" aria-disabled="true"', html)
        self.assertIn('id="last-page" aria-disabled="true"', html)

    def test_search_filters_by_title_and_content(self):
        response = self.client.get("/?q=파이썬")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("파이썬 검색 제목 15", html)
        self.assertIn("일반 제목", html)
        self.assertNotIn("테스트 글 1", html)
        self.assertIn("1 / 2", html)

    def test_search_no_results_shows_message(self):
        response = self.client.get("/?q=없는키워드")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("검색 결과가 없습니다", html)

    def test_search_pagination_keeps_query_string(self):
        response = self.client.get("/?q=파이썬&page=1")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("page=2&amp;q=%ED%8C%8C%EC%9D%B4%EC%8D%AC", html)

    def test_sort_dropdown_default_and_options(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('id="sort-select"', html)
        self.assertIn('value="latest" selected', html)
        self.assertIn('value="oldest"', html)
        self.assertIn('value="title_asc"', html)

    def test_sort_oldest_orders_by_oldest_first(self):
        response = self.client.get("/?sort=oldest")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.find("가나다 테스트") < html.find("나다라 테스트") < html.find("다라마 테스트"))
        self.assertNotIn("일반 제목", html)

    def test_sort_title_orders_by_korean_alphabet(self):
        response = self.client.get("/?sort=title_asc")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(html.find("가나다 테스트") < html.find("나다라 테스트") < html.find("다라마 테스트"))

    def test_sort_with_search_and_pagination_keeps_params(self):
        response = self.client.get("/?q=파이썬&sort=oldest&page=1")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("page=2", html)
        self.assertIn("q=%ED%8C%8C%EC%9D%B4%EC%8D%AC", html)
        self.assertIn("sort=oldest", html)
        self.assertIn('value="oldest" selected', html)


if __name__ == "__main__":
    unittest.main()
