CREATE TABLE users (
    id INTEGER PRIMARY KEY
);

CREATE TABLE borrowers (
    username VARCHAR PRIMARY KEY
);

CREATE TABLE money_owed (
    id INTEGER PRIMARY KEY,
    title TEXT,
    amount INTEGER,
    ah_long INTEGER,
    borrower VARCHAR
);