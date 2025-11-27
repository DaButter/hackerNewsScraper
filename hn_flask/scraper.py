import requests
from bs4 import BeautifulSoup

def fetch_articles_from_html_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    articles = []

    for tr in soup.select("tr.athing"):
        try:
            hn_id = int(tr["id"])
        except (KeyError, ValueError, TypeError):
            continue

        title_tag = tr.select_one("span.titleline > a")
        title = title_tag.get_text(strip=True) if title_tag else None
        # in case link is missing, set to None
        link = title_tag["href"] if title_tag and title_tag.has_attr("href") else None

        points = None
        created = None

        subtext_tr = tr.find_next_sibling("tr")
        if subtext_tr:
            # score id is in score_<hn_id>
            score_sel = subtext_tr.select_one(f"span.score#score_{hn_id}")
            if score_sel:
                score_text = score_sel.get_text(strip=True)
                # score_text f.e. "130 points" or "1 point"
                try:
                    points = int(score_text.split()[0].replace(",", ""))
                except Exception:
                    points = None

            age_sel = subtext_tr.select_one("span.age")
            if age_sel and age_sel.has_attr("title"):
                # title attr holds an ISO timestamp + epoch ("2025-11-27T10:54:02 1764240842")
                created = age_sel["title"].split()[0]

        articles.append({
            "id": hn_id,
            "title": title,
            "link": link,
            "points": points,
            "created_at": created,
        })

    return articles

def fetch_articles_from_pages():
    all_articles = []
    page = 1
    while True:
        url = f"https://news.ycombinator.com/?p={page}"
        print(f"Fetching page {page} ...")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}: {resp.status_code}")
            break
        articles = fetch_articles_from_html_page(resp.text)
        if not articles:
            print(f"No articles found on page {page}. Stopping.")
            break

        # TEST - limit the count of pages to avoid long runs for testing
        if page >= 2:
            print("[TEST]: Reached page limit for testing. Stopping.")
            break

        print(f"Found {len(articles)} articles on page {page}")
        all_articles.extend(articles)
        page += 1

    print(f"\nTotal articles found: {len(all_articles)}")
    return all_articles
