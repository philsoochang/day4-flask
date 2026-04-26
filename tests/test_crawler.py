import unittest
from unittest.mock import Mock, patch

import crawler


SAMPLE_RSS = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<rss version=\"2.0\">
  <channel>
    <title>Sample Feed</title>
    <item>
      <title>제목 1</title>
      <description>요약 1</description>
      <link>https://example.com/1</link>
      <pubDate>Sun, 26 Apr 2026 09:00:00 +0900</pubDate>
    </item>
    <item>
      <title>제목 2</title>
      <description><![CDATA[<p>요약 <b>2</b></p>]]></description>
      <link>https://example.com/2</link>
      <pubDate>Sun, 26 Apr 2026 08:30:00 +0900</pubDate>
    </item>
  </channel>
</rss>
"""


class CrawlerTests(unittest.TestCase):
    @patch("crawler.requests.get")
    def test_fetch_news_items_parses_title_summary_link_and_pubdate(self, mock_get):
        response = Mock()
        response.content = SAMPLE_RSS.encode("utf-8")
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        items = crawler.fetch_news_items("https://example.com/rss", limit=10)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "제목 1")
        self.assertEqual(items[0]["summary"], "요약 1")
        self.assertEqual(items[0]["link"], "https://example.com/1")
        self.assertEqual(items[0]["published"], "Sun, 26 Apr 2026 09:00:00 +0900")
        self.assertEqual(items[1]["summary"], "요약 2")

    @patch("crawler.requests.get")
    def test_fetch_news_items_respects_limit(self, mock_get):
        many_items = "".join(
            f"""
            <item>
              <title>제목 {i}</title>
              <description>요약 {i}</description>
              <link>https://example.com/{i}</link>
              <pubDate>Sun, 26 Apr 2026 09:{i:02d}:00 +0900</pubDate>
            </item>
            """
            for i in range(1, 15)
        )
        rss = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<rss version=\"2.0\"><channel>{many_items}</channel></rss>"""

        response = Mock()
        response.content = rss.encode("utf-8")
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        items = crawler.fetch_news_items("https://example.com/rss", limit=10)

        self.assertEqual(len(items), 10)
        self.assertEqual(items[-1]["title"], "제목 10")


if __name__ == "__main__":
    unittest.main()
