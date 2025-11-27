https://github.com/HackerNews/API?tab=readme-ov-file - HN official API readme
HTML: does not conain 

Run:
```
python -m flask --app app scrape-ids-json
docker-compose up -d
pip install -r requirements.txt
python -m flask --app hn_flask.app scrape-ids-db
```