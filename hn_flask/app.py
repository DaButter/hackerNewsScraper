from flask import Flask, jsonify, render_template
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
        created_at = None
        created_val = item.get("created_at")
        if isinstance(created_val, str) and created_val:
            try:
                created_at = datetime.datetime.fromisoformat(created_val)
            except ValueError:
                created_at = None

        article = session.query(Article).filter_by(id=item["id"]).first()
        if article:
            article.points = item.get("points", article.points)

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


@app.route("/api/articles")
def api_articles():
    session = SessionLocal()
    articles = session.query(Article).all()
    result = []
    for a in articles:
        result.append({
            "id": a.id,
            "title": a.title,
            "link": a.link,
            "points": a.points,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        })
    session.close()
    return jsonify(result)


@app.route("/")
def index():
    return render_template("index.html")
