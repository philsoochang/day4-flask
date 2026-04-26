import requests
from bs4 import BeautifulSoup

RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"


def _extract_text(node):
    if not node:
        return ""

    raw_text = node.get_text(" ", strip=True)
    if "<" in raw_text and ">" in raw_text:
        return BeautifulSoup(raw_text, "html.parser").get_text(" ", strip=True)
    return raw_text


def fetch_news_items(url=RSS_URL, limit=10):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    items = []

    for item in soup.find_all("item")[:limit]:
        title = _extract_text(item.find("title"))
        summary = _extract_text(item.find("description"))
        link = _extract_text(item.find("link"))
        published = _extract_text(item.find("pubDate"))

        items.append(
            {
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
            }
        )

    return items


def print_items(items):
    for i, item in enumerate(items, start=1):
        short_summary = item["summary"][:70] + ("..." if len(item["summary"]) > 70 else "")
        print(f"[{i:02}] {item['title']}")
        print(f"     {item['published']} | {short_summary}")
        print(f"     {item['link']}")


def main():
    news_items = fetch_news_items(limit=10)
    print_items(news_items)


if __name__ == "__main__":
    main()
