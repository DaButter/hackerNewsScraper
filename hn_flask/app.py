from flask import Flask
from scraper import fetch_ids_from_pages, fetch_articles_json
from models import Article, SessionLocal, init_db
import datetime

app = Flask(__name__)

@app.cli.command("scrape-ids-db")
def scrape_ids_db():
    # scrape HN articles and save to PostgreSQL DB
    init_db()
    session = SessionLocal()

    news_ids_list = fetch_ids_from_pages()
    articles_json = fetch_articles_json(news_ids_list)

    for item in articles_json:
        created_at = datetime.datetime.fromtimestamp(item.get("time", 0))
        article = session.query(Article).filter_by(id=item["id"]).first()
        if article:
            article.points = item.get("score", 0)
        else:
            article = Article(
                id=item["id"],
                title=item.get("title", ""),
                url=item.get("url", ""),
                points=item.get("score", 0),
                created_at=created_at
            )
            session.add(article)

    session.commit()
    print(f"Saved/Updated {len(articles_json)} articles in database.")
    session.close()
