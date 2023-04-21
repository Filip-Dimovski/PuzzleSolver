create table user(
id int not null auto_increment primary key,
user_name nvarchar(200),
password nvarchar(500),
created_date datetime default NOW(),
modified_date datetime
);


create table puzzle(
id int not null auto_increment primary key,
name nvarchar(200),
full_image_path nvarchar(1000),
parts_image_path nvarchar(1000),
created_date datetime  default NOW(),
created_by nvarchar(200),
modified_date datetime,
modified_by nvarchar(200)
);


create table user_puzzle(
user_id int,
puzzle_id int,
foreign key (user_id) references user(Id) ON UPDATE CASCADE ON DELETE RESTRICT,
foreign key (puzzle_id) references puzzle(Id) ON UPDATE CASCADE ON DELETE RESTRICT,
);


ALTER TABLE puzzle
ADD COLUMN solution_image_path nvarchar(1000) AFTER parts_image_path;