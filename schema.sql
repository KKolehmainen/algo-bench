CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE algorithms (
    id INTEGER PRIMARY KEY,
    name TEXT,
    source_code TEXT,
    username TEXT
);