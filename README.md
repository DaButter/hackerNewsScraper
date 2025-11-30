# Prerequisites

* Docker desktop
* In normal development `.env` should not be committed!

# How to start the application

From project root directory run the following commands:

1. `docker-compose up -d --build`
   - Sets up PostgresDB, installs Python dependencies, and starts the application.  
   - Application will be available at: [http://localhost:5000](http://localhost:5000)

2. `docker-compose run --rm web pytest -q`
   - Run all unit tests in the `tests/` folder.

3. `docker-compose run --rm web flask scrape-articles`
   - Scrapes article data from `https://news.ycombinator.com/`.
   - Subsequent calls add new articles and update existing ones in the database.

4. `docker-compose down`
   - Stop the application and containers. Data persists in the Postgres volume unless explicitly removed.


# Why not use public API for scraping?

Hacker News has a public API ```https://github.com/HackerNews/API?tab=readme-ov-file```.

Even if we scrape all news article unique IDs (which is ~800 at the moment), we still need to parse IDs one by one to the API. There is not an option to parse a list of IDs.

API returns a beautiful JSON (for example, ```https://hacker-news.firebaseio.com/v0/item/46068015.json?print=pretty```), if we provide an article ID:
```json
{
  "by": "PikelEmi",
  "descendants": 156,
  "id": 46068015,
  "kids": [46070181, 46068204, 46068275, 46068951, 46068691, 46069430, 46069543, 46068869, 46068861, 46069124, 46068456, 46069069],
  "score": 133,
  "time": 1764240842,
  "title": "Arthur Conan Doyle explored men’s mental health through Sherlock Holmes",
  "type": "story",
  "url": "https://scienceclock.com/arthur-conan-doyle-delved-into-mens-mental-health-through-his-sherlock-holmes-stories/"
}
```
The N count of HTTP requests is a big performance bottleneck. So I chose to stick to scraping from raw HTML with bs4 library.

# Useful

Log into DB:
```bash
docker-compose exec db psql -U hn_user -d hn_db

# Once inside psql:
\dt                     # list all tables
SELECT * FROM articles; # view articles table data
\d articles             # describe articles table structure
\q                      # exit psql
```

Stop and remove container + db volume:
```bash
docker-compose down -v
```
