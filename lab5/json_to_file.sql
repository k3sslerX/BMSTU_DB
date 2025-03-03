-- Загружаем данные в файл
\copy (select row_to_json(c) from cars c) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars.json';
\copy (select row_to_json(s) from showrooms s) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/showrooms.json';
\copy (select row_to_json(e) from engines e) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/engines.json';
\copy (select row_to_json(c_e) from cars_engines c_e) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars_engines.json';
\copy (select row_to_json(p) from cars_prices p) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/prices.json';
\copy (select row_to_json(c_e_s) from cars_engines_showrooms c_e_s) to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars_engines_showrooms.json';