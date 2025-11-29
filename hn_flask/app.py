from flask import Flask, jsonify, render_template, request
from scraper import fetch_articles_from_pages
from models import Article, SessionLocal, init_db
import datetime
from sqlalchemy import func, or_, desc, asc

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
    # DataTables server-side processing
    draw = int(request.args.get("draw", "1"))
    start = int(request.args.get("start", "0"))
    length = int(request.args.get("length", "10"))
    search_value = request.args.get("search[value]", "").strip()

    # map DataTables column index to model attribute
    cols = {
        0: Article.id,
        1: Article.title,
        2: Article.link,
        3: Article.points,
        4: Article.created_at,
    }

    order_col_index = request.args.get("order[0][column]")
    order_dir = request.args.get("order[0][dir]", "desc")

    session = SessionLocal()
    total_count = session.query(func.count(Article.id)).scalar()

    query = session.query(Article)
    if search_value:
        pattern = f"%{search_value}%"
        query = query.filter(or_(Article.title.ilike(pattern), Article.link.ilike(pattern)))

    filtered_count = query.with_entities(func.count(Article.id)).scalar()

    try:
        if order_col_index is not None:
            col_index = int(order_col_index)
            col = cols.get(col_index, Article.points)
            if order_dir == "asc":
                query = query.order_by(asc(col))
            else:
                query = query.order_by(desc(col))
        else:
            query = query.order_by(desc(Article.points))
    except Exception:
        query = query.order_by(desc(Article.points))

    items = query.offset(start).limit(length).all()

    data = []
    for a in items:
        data.append([
            a.id,
            a.title,
            a.link or "",
            a.points if a.points is not None else 0,
            a.created_at.isoformat() if a.created_at else "",
        ])

    session.close()

    return jsonify({
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": data,
    })


@app.route("/")
def index():
    return render_template("index.html")
