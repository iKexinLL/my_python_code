create table IF NOT EXISTS people_info (
  username TEXT UNIQUE ,
  password TEXT,
  nickname TEXT DEFAULT NULL
);

