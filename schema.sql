-- SQL commands used to initialize envirohub.db

-- Create users table and corresponding username index
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);

-- Create forecast history table and corresponding user id index
CREATE TABLE IF NOT EXISTS fc_history (
    user_id INTEGER,
    datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lat NUMERIC NOT NULL,
    lon NUMERIC NOT NULL,
    temp NUMERIC NOT NULL,
    weather TEXT NOT NULL,
    aqi INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS user_id ON fc_history (user_id);

