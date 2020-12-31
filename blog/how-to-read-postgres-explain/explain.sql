DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS articles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users(id INTEGER PRIMARY KEY, email VARCHAR(100));
CREATE TABLE articles(id INTEGER PRIMARY KEY, name VARCHAR(100));
CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    article_id INTEGER REFERENCES articles(id),
    qty INTEGER
);

--CREATE UNIQUE INDEX users_email_index ON users(email);

--CREATE INDEX orders_userid_index ON orders(user_id);
--CREATE INDEX orders_articleid_index ON orders(article_id);

INSERT INTO users(id, email) VALUES(1, 'jon@example.com');
INSERT INTO users(id, email) VALUES(2, 'Jane@example.com');

INSERT INTO articles(id, name) VALUES(1, 'Playstation');
INSERT INTO articles(id, name) VALUES(2, 'Xbox');

INSERT INTO orders(id, user_id, article_id, qty) VALUES(1, 1, 1, 2);
INSERT INTO orders(id, user_id, article_id, qty) VALUES(2, 1, 2, 1);
INSERT INTO orders(id, user_id, article_id, qty) VALUES(3, 2, 1, 4);
INSERT INTO orders(id, user_id, article_id, qty) VALUES(4, 2, 2, 3);

SELECT * FROM users;
SELECT * FROM articles;
SELECT * FROM orders;


EXPLAIN SELECT * FROM users WHERE email='jon@example.com';

-- SET enable_seqscan = OFF;
-- SET enable_bitmapscan = OFF;

EXPLAIN SELECT * FROM users WHERE email='jon@example.com';

EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    WHERE users.email='jon@example.com';

EXPLAIN SELECT *
    FROM orders
    INNER JOIN users
        ON orders.user_id=users.id
    INNER JOIN articles
        ON orders.article_id=articles.id
    WHERE users.email='jon@example.com';

