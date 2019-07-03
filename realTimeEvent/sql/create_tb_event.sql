/*
 * Run this file 2nd
 */

DROP TABLE IF EXISTS tb_event;
DROP SEQUENCE IF EXISTS event_seq;

CREATE SEQUENCE event_seq;

CREATE TABLE tb_event (
    event INTEGER PRIMARY KEY DEFAULT nextval('event_seq'),
    hashtag VARCHAR,
    tweet VARCHAR,
    cell VARCHAR,
    created TIMESTAMP DEFAULT Now(),
    is_event_cell BOOLEAN DEFAULT 't'
);





