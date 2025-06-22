create schema gym;

CREATE TABLE gym.user (
	user_id serial PRIMARY KEY,
	username text NOT null unique,
	phone text not null unique,
	first_name text NULL,
	last_name text NULL,
	email text unique,
	telegram_id int8 NOT NULL
);


CREATE TABLE gym.master (
	user_id int references gym.user(user_id),
	master_id serial PRIMARY KEY,
	create_dttm timestamptz NOT NULL,
	is_active bool DEFAULT true
);


CREATE TABLE gym.gymer (
	gymer_id serial PRIMARY KEY,
	user_id int references gym.user(user_id),
	create_dttm timestamptz NOT NULL,
	is_active bool DEFAULT true
);

create table gym.master_gym (
	master_id int references gym.master(master_id),
	gymer_id int references gym.gymer(gymer_id),
	create_dttm timestamptz not null,
	close_dttm timestamptz
);

create table gym.exercise (
	exercise_id serial primary key,
	master_id int references gym.master(master_id),
	title text not null
);

create table gym.exercise_desc (
	exercise_desc_id serial primary key,
	exercise_id int references gym.exercise(exercise_id),
	description text not null
);


create table gym.card (
	card_id serial primary key,
	master_id int references gym.master(master_id),
	create_dttm timestamptz not null,
	update_dttm timestamptz,
	status varchar(15) not null default 'active',
	title varchar(45)
);

create table gym.link (
	link_id serial primary key,
	card_id int references gym.card(card_id),
	link TEXT NOT NULL,
	title text,
	create_dttm timestamptz not null,
	status varchar(15) not null default 'active'
);

create table gym.task_group (
	task_group_id serial primary key,
	master_id int REFERENCES gym.master(master_id),
	gymer_id int references gym.gymer(gymer_id),
	properties jsonb,
	status varchar(15) not null default 'planed',
	create_dttm timestamptz not null default now(),
	update_dttm timestamptz,
	start_dttm timestamptz,
	order_idx int
);

create table gym.task (
	task_id serial primary key,
	task_group_id int references gym.task_group(task_group_id),
	exercise_desc_id int references gym.exercise_desc(exercise_desc_id),
	properties jsonb,
	status varchar(15) not null default 'planed',
	create_dttm timestamptz not null default now(),
	update_dttm timestamptz,
	order_idx int
);

create table gym.card (
	card_id serial primary key,
	master_id int REFERENCES gym.master(master_id),
	create_dttm timestamptz not null default now(),
	status varchar(15) not null default 'active',
	update_dttm timestamptz,
	exercise_desc_id int references gym.exercise_desc(exercise_desc_id),

);


-- SELECT setval(
--     pg_get_serial_sequence('master', 'master_id'), 
--     COALESCE((SELECT MAX(master_id) FROM master), 0) + 1, 
--     false
-- );

-----------------------------




-- create table task_group_history (
-- 	task_group_id int references gym.task_group(task_group_id),
-- 	parent int references gym.task_group(task_group_id),
-- 	status text not null, --fixed, planning
-- 	CONSTRAINT check_same_gymer_constraint CHECK (check_same_gymer(task_group_id, parent_id));
-- )

-- CREATE OR REPLACE FUNCTION check_same_gymer(
--     p_task_group_id INT,
--     p_parent_id INT
-- ) RETURNS BOOLEAN AS $$
-- BEGIN
--     IF p_parent_id = p_task_group_id THEN
--         RETURN TRUE;
--     END IF;
    
--     RETURN (
--         SELECT g1.gymer_id = g2.gymer_id
--         FROM gym.task_group g1
--         JOIN gym.task_group g2 ON g2.task_group_id = p_parent_id
--         WHERE g1.task_group_id = p_task_group_id
--     );
-- END;
-- $$ LANGUAGE plpgsql;

-- ALTER TABLE gym.task_group_history
-- ADD 