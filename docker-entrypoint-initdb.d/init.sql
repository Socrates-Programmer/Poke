
CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(85) NOT NULL,
    last_name VARCHAR(36) NOT NULL,
    email VARCHAR(90) UNIQUE NOT NULL,
    password VARCHAR(350) NOT NULL,
    imagen LONGBLOB
);

CREATE TABLE IF NOT EXISTS user_post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    users_id_post INT,
    FOREIGN KEY (users_id_post) REFERENCES users(id_user)
);

CREATE TABLE IF NOT EXISTS notification (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receptor_id INT,
    sender_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receptor_id) REFERENCES users(id_user),
    FOREIGN KEY (sender_id) REFERENCES users(id_user)
);
