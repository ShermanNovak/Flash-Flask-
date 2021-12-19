CREATE TABLE IF NOT EXISTS users (
	user_id INTEGER NOT NULL,
	username TEXT UNIQUE NOT NULL,
	hash TEXT NOT NULL,
	PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS decks (
	user_id INTEGER NOT NULL,
	deck_id INTEGER NOT NULL,
	deck_name TEXT NOT NULL,
	deck_size INTEGER NOT NULL,
	timing TIMESTAMP,
	PRIMARY KEY(deck_id),
	FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS cards (
	user_id INTEGER NOT NULL,
	deck_name TEXT NOT NULL,
	deck_id INTEGER NOT NULL,
	card_id INTEGER NOT NULL,
	title TEXT NOT NULL,
	content TEXT NOT NULL,
	status TEXT,
	FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(deck_id) REFERENCES decks(deck_id)
);

DROP TABLE users;
DROP TABLE decks;
DROP TABLE cards;
