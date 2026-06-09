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

CREATE TABlE algorithm_classes (
    id INTEGER PRIMARY KEY,
    algo_id INTEGER REFERENCES algorithms,
    title TEXT,
    value TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    algo_id INTEGER REFERENCES algorithms,
    title TEXT,
    value TEXT
)