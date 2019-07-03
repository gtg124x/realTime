/*
 * Run this file 2nd
 */

DROP TABLE IF EXISTS tb_rawdata;
DROP SEQUENCE IF EXISTS rawdata_seq;

CREATE SEQUENCE rawdata_seq;

CREATE TABLE tb_rawdata (
    rawdata INTEGER PRIMARY KEY DEFAULT nextval('rawdata_seq'),
    created TIMESTAMP DEFAULT Now(),
    tweet JSON
);


