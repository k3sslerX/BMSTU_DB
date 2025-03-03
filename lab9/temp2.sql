-- Назначение прав на все объекты в базе данных musicians
GRANT ALL PRIVILEGES ON DATABASE musicians TO hleb;

-- Даем все права на все таблицы в схеме public (если используется схема public)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hleb;

-- Даем все права на все последовательности в схеме public
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hleb;

-- Даем все права на все функции в схеме public
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO hleb;

-- Обновляем дефолтные привилегии для новых объектов в схеме public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO hleb;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO hleb;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO hleb;

GRANT ALL PRIVILEGES ON TABLE artists TO hleb;
GRANT ALL PRIVILEGES ON TABLE albums TO hleb;
GRANT ALL PRIVILEGES ON TABLE labels TO hleb;
GRANT ALL PRIVILEGES ON TABLE songs TO hleb;