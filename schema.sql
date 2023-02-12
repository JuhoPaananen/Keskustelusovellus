CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin BOOLEAN DEFAULT FALSE,
    insider BOOLEAN
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    secret BOOLEAN DEFAULT FALSE
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    category_id INT NOT NULL REFERENCES categories(id),
    title TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    topic_id INT NOT NULL REFERENCES topics(id),
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW(),
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    message_id INT NOT NULL REFERENCES messages(id),
    vote INT DEFAULT 1
);