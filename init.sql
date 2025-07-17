-- poke_users.sql
CREATE TABLE IF NOT EXISTS users (
    id_user SERIAL PRIMARY KEY,
    name VARCHAR(85) NOT NULL,
    last_name VARCHAR(36) NOT NULL,
    email VARCHAR(90) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    imagen BYTEA
);

-- poke_user_post.sql
CREATE TABLE IF NOT EXISTS user_post (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    users_id_post INTEGER REFERENCES users(id_user)
);

-- poke_notification.sql
CREATE TABLE IF NOT EXISTS notification (
    id SERIAL PRIMARY KEY,
    receptor_id INTEGER REFERENCES users(id_user),
    sender_id INTEGER REFERENCES users(id_user),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
