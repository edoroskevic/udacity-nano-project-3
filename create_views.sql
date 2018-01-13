CREATE OR REPLACE VIEW errors AS
SELECT time::date, COUNT(status) FROM log WHERE status LIKE '%404%'
GROUP BY time::date;

CREATE OR REPLACE VIEW totals AS
SELECT time::date, COUNT(status) FROM log GROUP BY time::date;
