--upon insert to tb_event, mark owned if the hashtag is first used in this 1hr data set (now -1hr )
--when inserting row, mark as not owned if for this interval if there is there exists an entry where hashtags are == & cells are != & owned is TRUE
CREATE OR REPLACE FUNCTION fn_update_is_event_cell()
RETURNS VOID AS
$$
BEGIN

    CREATE TEMPORARY TABLE IF NOT EXISTS temp_table AS
    SELECT distinct on (hashtag) hashtag, is_event_cell, created, cell, event
      FROM tb_event WHERE inserted >= CURRENT_TIMESTAMP - INTERVAL '2 minutes'
  ORDER BY hashtag, created asc;

    Update tb_event
    SET is_event_cell = 't'
    FROM temp_table
    WHERE temp_table.hashtag = tb_event.hashtag
      AND temp_table.created = tb_event.created
      AND temp_table.cell    = tb_event.cell;

    DROP TABLE temp_table;

END;
$$
LANGUAGE plpgsql;

