
drop table if exists posts;
create table posts  (
    id integer primary key autoincrement,
    title string,
    text string,
    url string,
    code string,
    contenttype integer,

    time string not null,
    user string not null
);

drop table if exists comments;
create table comments   (
    id integer primary key autoincrement,
    content string not null,
    post integer not null,
    user string not null,

    time string not null
);

drop table if exists users;
create table users  (
    id integer primary key autoincrement,

    name string not null,
    password string not null,
    email string not null,

    admin integer not null,
    active integer not null,
    lastlogin string,
    postspersite integer not null,
    emailnotification integer not null,
    rememberme integer not null,

    avatar string,
    style string,
    template string
);
