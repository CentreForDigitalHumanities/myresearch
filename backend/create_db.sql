create user myresearch with createdb password 'myresearch';
create database myresearch owner myresearch;
grant all on database myresearch to myresearch;
grant all on schema public to myresearch;
