\set age random(1, 95)
select * from day_result where age = :age and datestr='20190610' offset 10000 limit 100;