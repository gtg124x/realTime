CREATE OR REPLACE VIEW vw_events AS
WITH tt_expected AS
(
  SELECT hashtag,
         array_agg(tweet) AS tweet,
         COUNT (tweet) AS expected,
         array_agg(created) AS created
    FROM tb_event
   WHERE created < CURRENT_TIMESTAMP - INTERVAL '1 hours'
     AND created >= CURRENT_TIMESTAMP - INTERVAL '25 hours'
GROUP BY hashtag
ORDER BY expected desc
LIMIT 500
),
tt_observed AS
(
  SELECT hashtag,
         array_agg(tweet) AS tweet,
         COUNT (tweet) AS observed,
         array_agg(created) AS created
    FROM tb_event
   WHERE created < CURRENT_TIMESTAMP
     AND created >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY hashtag
ORDER BY observed desc
LIMIT 500
),
tt_obs_minus_exp AS
(
SELECT tto.hashtag,
       array_agg(tto.tweet) AS tweet,
       array_agg(tto.created) AS created,
       sum(tto.observed - tte.expected) AS numerator,
       tte.expected AS expected
FROM tt_observed tto
LEFT JOIN tt_expected tte
ON tto.hashtag = tte.hashtag
GROUP BY tto.hashtag, tte.expected
),
tt_fraction_setup AS
(
SELECT hashtag,
       tweet,
       created,
       numerator * numerator AS numerator_squared,
       case when expected = 0 then expected else expected
       end as expected
  FROM tt_obs_minus_exp
 WHERE numerator > 0
),
tt_chi AS
(
SELECT hashtag,
       tweet,
       created,
       numerator_squared,
       expected,
       numerator_squared / expected AS chi
  FROM tt_fraction_setup
),
tt_events AS
(
SELECT ttc.hashtag,
       ttc.tweet,
       ttc.created,
       ttc.numerator_squared,
       ttc.expected,
       ttc.chi,
       tbe.cell
  FROM tt_chi ttc
LEFT JOIN tb_event tbe
     ON ttc.hashtag = tbe.hashtag
  WHERE tbe.is_event_cell = 't'
),
tt_current_events AS
(
SELECT hashtag,
       inserted
  FROM tb_event
 WHERE inserted > CURRENT_TIMESTAMP - INTERVAL '1 hours'
   AND is_event_cell = 't'
)
SELECT tte.hashtag,
       tte.tweet,
       tte.cell
  FROM tt_events tte
  inner join tt_current_events ttce
 on tte.hashtag = ttce.hashtag
;
