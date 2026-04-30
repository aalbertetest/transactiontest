CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE posts (
    id          SERIAL PRIMARY KEY,
    author_id   INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(255) NOT NULL,
    body        TEXT         NOT NULL,
    published   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE comments (
    id          SERIAL PRIMARY KEY,
    post_id     INTEGER      NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id   INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body        TEXT         NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_posts_author    ON posts(author_id);
CREATE INDEX idx_comments_post   ON comments(post_id);
CREATE INDEX idx_comments_author ON comments(author_id);
