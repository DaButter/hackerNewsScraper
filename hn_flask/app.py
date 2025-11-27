from flask import Flask
from scraper import fetch_articles_from_pages
from models import Article, SessionLocal, init_db
import datetime

app = Flask(__name__)

@app.cli.command("scrape-ids")
def scrape_ids():
    init_db()
    session = SessionLocal()

    news_articles = fetch_articles_from_pages()
    print(f"First article returned: {news_articles[0] if news_articles else 'No articles fetched'}")
    # print(f"[DEBUG] Articles fetched: {(news_articles)}")

    for item in news_articles:
        created_at = datetime.datetime.fromisoformat(item.get("created_at", "1970-01-01T00:00:00"))
        article = session.query(Article).filter_by(id=item["id"]).first()
        if article:
            article.points = item.get("points", 0)
        else:
            article = Article(
                id=item["id"],
                title=item.get("title", ""),
                link=item.get("link", ""),
                points=item.get("points", 0),
                created_at=created_at
            )
            session.add(article)

    session.commit()
    print(f"Saved/Updated {len(news_articles)} articles in database.")
    session.close()
