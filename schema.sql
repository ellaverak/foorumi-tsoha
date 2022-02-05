CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    secret INTEGER,
    user_id INTEGER
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    op_content TEXT,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE replys (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE secret (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE
);
