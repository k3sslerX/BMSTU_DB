-- Создание пользователя hleb с паролем 4572
CREATE USER hleb WITH PASSWORD '4572';

-- Назначение прав на подключение к базе данных musicians
GRANT CONNECT ON DATABASE musicians TO hleb;
