CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    op_content TEXT,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE replys (
    id SERIAL PRIMARY KEY,
    content TEXT,
    thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
