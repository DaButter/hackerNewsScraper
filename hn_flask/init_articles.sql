CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    link TEXT,
    points INTEGER DEFAULT 0,
    created_at TIMESTAMP
);
