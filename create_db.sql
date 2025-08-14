CREATE USER myresearch WITH createdb PASSWORD 'myresearch';
CREATE DATABASE myresearch;
GRANT ALL ON DATABASE myresearch TO myresearch;
GRANT ALL ON SCHEMA public TO myresearch;
ALTER DATABASE myresearch OWNER TO myresearch;
