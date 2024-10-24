CREATE TYPE public.remindertype AS ENUM
    ('QUIZ', 'ASSIGN', 'PAGE');





-- Type: typerolechoices

-- DROP TYPE IF EXISTS public.typerolechoices;

CREATE TYPE public.typerolechoices AS ENUM
    ('BOT', 'USER');




CREATE SEQUENCE IF NOT EXISTS public.messages_chatbot_deleted_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE SEQUENCE IF NOT EXISTS public.messages_chatbot_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;


CREATE SEQUENCE IF NOT EXISTS public.messages_reminders_chatbot_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;
    


CREATE TABLE IF NOT EXISTS public.messages_chatbot
(
    created_at timestamp without time zone,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    "chatId" integer NOT NULL,
    role typerolechoices NOT NULL,
    id integer NOT NULL DEFAULT nextval('messages_chatbot_id_seq'::regclass),
    CONSTRAINT messages_chatbot_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;



-- Table: public.messages_chatbot_deleted

-- DROP TABLE IF EXISTS public.messages_chatbot_deleted;

CREATE TABLE IF NOT EXISTS public.messages_chatbot_deleted
(
    created_at timestamp without time zone,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    "chatId" integer NOT NULL,
    role typerolechoices NOT NULL,
    id integer NOT NULL DEFAULT nextval('messages_chatbot_deleted_id_seq'::regclass),
    CONSTRAINT messages_chatbot_deleted_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;


-- Table: public.messages_reminders_chatbot

-- DROP TABLE IF EXISTS public.messages_reminders_chatbot;

CREATE TABLE IF NOT EXISTS public.messages_reminders_chatbot
(
    created_at timestamp without time zone,
    id integer NOT NULL DEFAULT nextval('messages_reminders_chatbot_id_seq'::regclass),
    type character varying COLLATE pg_catalog."default" NOT NULL,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    "chatId" integer NOT NULL,
    time_remind timestamp without time zone NOT NULL,
    is_remind boolean NOT NULL,
    CONSTRAINT messages_reminders_chatbot_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;




--- create table embedding
CREATE EXTENSION IF NOT EXISTS vector

CREATE TABLE embeddings_v2 (
            id bigserial primary key,
            courseId interger,
            title text,
            url text,
            content text,
            tokens integer,
            embedding vector(768)
            )
ALTER TABLE embeddings_v2
ADD CONSTRAINT unique_url UNIQUE (url);


---
create or replace function get_course_of_user(user_id int)
  returns table (course_id int8, course_name text)
as
$body$
  SELECT c.id AS course_id, c.fullname
                            FROM mdl_user u
                            JOIN mdl_user_enrolments ue ON u.id = ue.userid
                            JOIN mdl_enrol e ON ue.enrolid = e.id
                            JOIN mdl_course c ON e.courseid = c.id
                            WHERE u.id = $1
                            ORDER BY ue.timestart DESC
                            LIMIT 5;
$body$
language sql;

select get_course_of_user(3)
