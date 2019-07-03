/*
 * Run this file 2nd
 */

DROP TABLE IF EXISTS tb_rawData;
DROP SEQUENCE IF EXISTS rawData_seq;

CREATE SEQUENCE rawData_seq;

CREATE TABLE tb_rawdata (
    rawData INTEGER PRIMARY KEY DEFAULT nextval('rawData_seq'),
    created TIMESTAMP DEFAULT Now(),
    tweet JSON
);


