# scraper.py
import requests
from bs4 import BeautifulSoup

HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"

def fetch_ids_from_html_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    ids = [int(tr["id"]) for tr in soup.select("tr.athing")]
    return ids

def fetch_ids_from_pages():
    all_ids = []
    page = 1
    while True:
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"Fetching page {page} ...")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}: {resp.status_code}")
            break

        ids = fetch_ids_from_html_page(resp.text)
        if not ids:
            print(f"No articles found on page {page}. Stopping.")
            break

        # TEST - limit the count of pages to avoid long runs for testing
        if page >= 2:
            print("[TEST]: Reached page limit for testing. Stopping.")
            break

        print(f"Found {len(ids)} article IDs on page {page}")
        all_ids.extend(ids)
        page += 1

    print(f"\nTotal article IDs found: {len(all_ids)}")
    return all_ids

def fetch_article_json(hn_id):
    url = HN_ITEM_URL.format(hn_id)
    resp = requests.get(url)
    if resp.status_code == 200:
        print(f"Fetched article {hn_id}")
        return resp.json()
    else:
        print(f"Failed to fetch article {hn_id}: {resp.status_code}")
        return None

# use news IDs list to fetch article JSONs using HN API
def fetch_articles_json(ids_list):
    print("\nFetching article JSONs ...")
    articles = []
    for hn_id in ids_list:
        article = fetch_article_json(hn_id)
        if article:
            articles.append(article)
    print(f"\nTotal articles fetched: {len(articles)}")
    return articles
