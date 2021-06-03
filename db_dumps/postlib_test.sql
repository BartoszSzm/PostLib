--
-- PostgreSQL database dump
--

-- Dumped from database version 11.10 (Raspbian 11.10-0+deb10u1)
-- Dumped by pg_dump version 11.10 (Raspbian 11.10-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: calculate_delay(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.calculate_delay() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN 
IF NEW.returned_date > OLD.issue_limit THEN
UPDATE issue SET delay = (NEW.returned_date - OLD.issue_limit) WHERE issue_id=NEW.issue_id;
END IF;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.calculate_delay() OWNER TO pi;

--
-- Name: change_issued(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.change_issued() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN 
UPDATE publications SET is_issued = 'true' WHERE lib_id=NEW.lib_id;
RETURN NEW;
END;
$$;


ALTER FUNCTION public.change_issued() OWNER TO pi;

--
-- Name: change_issued_delete(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.change_issued_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

UPDATE publications SET is_issued = 'false' WHERE lib_id=OLD.lib_id; 

RETURN NEW;
END;
$$;


ALTER FUNCTION public.change_issued_delete() OWNER TO pi;

--
-- Name: change_issued_return(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.change_issued_return() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

IF NEW.returned_date IS NOT NULL THEN
UPDATE publications SET is_issued = 'false' WHERE lib_id=NEW.lib_id;
END IF;

RETURN NEW;
END;
$$;


ALTER FUNCTION public.change_issued_return() OWNER TO pi;

--
-- Name: issue_when_not_issued(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.issue_when_not_issued() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
       IF (SELECT is_issued FROM publications WHERE lib_id=NEW.lib_id) = True THEN
          raise unique_violation using detail = 'Publication with this lib_id is alredy issued and was not returned';
       ELSE RETURN NEW;
        END IF;

END;
$$;


ALTER FUNCTION public.issue_when_not_issued() OWNER TO pi;

--
-- Name: sum_penalties(); Type: FUNCTION; Schema: public; Owner: pi
--

CREATE FUNCTION public.sum_penalties() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN 
UPDATE person SET total_penalty=(SELECT SUM(imposed_penalty) FROM issue WHERE reader_id = OLD.reader_id);
RETURN NEW;
END;
$$;


ALTER FUNCTION public.sum_penalties() OWNER TO pi;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: issue; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.issue (
    issue_id bigint NOT NULL,
    lib_id bigint NOT NULL,
    reader_id bigint NOT NULL,
    issue_date date DEFAULT now() NOT NULL,
    issue_limit date NOT NULL,
    returned_date date,
    delay integer,
    imposed_penalty numeric(10,2),
    CONSTRAINT larger_than_now CHECK (((issue_limit > issue_date) AND (returned_date >= issue_date)))
);


ALTER TABLE public.issue OWNER TO pi;

--
-- Name: issue_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.issue_issue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issue_issue_id_seq OWNER TO pi;

--
-- Name: issue_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public.issue_issue_id_seq OWNED BY public.issue.issue_id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.person (
    reader_id bigint NOT NULL,
    full_name character varying(50) NOT NULL,
    phone_number character varying(50),
    email character varying(50),
    id_card character varying(50) NOT NULL,
    total_penalty numeric(10,2),
    CONSTRAINT "not empty" CHECK ((((full_name)::text <> ''::text) AND ((id_card)::text <> ''::text)))
);


ALTER TABLE public.person OWNER TO pi;

--
-- Name: person_reader_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.person_reader_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.person_reader_id_seq OWNER TO pi;

--
-- Name: person_reader_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public.person_reader_id_seq OWNED BY public.person.reader_id;


--
-- Name: publications; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.publications (
    lib_id bigint NOT NULL,
    title character varying(200) NOT NULL,
    author character varying(100) NOT NULL,
    kind character varying(100),
    publisher character varying(100) NOT NULL,
    year_of_publish integer NOT NULL,
    language character varying(50),
    pages character varying(20),
    isbn character varying(50),
    is_issued boolean DEFAULT false NOT NULL,
    CONSTRAINT "not empty" CHECK ((((title)::text <> ''::text) AND ((author)::text <> ''::text) AND ((publisher)::text <> ''::text)))
);


ALTER TABLE public.publications OWNER TO pi;

--
-- Name: publications_lib_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE public.publications_lib_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.publications_lib_id_seq OWNER TO pi;

--
-- Name: publications_lib_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE public.publications_lib_id_seq OWNED BY public.publications.lib_id;


--
-- Name: issue issue_id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.issue ALTER COLUMN issue_id SET DEFAULT nextval('public.issue_issue_id_seq'::regclass);


--
-- Name: person reader_id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.person ALTER COLUMN reader_id SET DEFAULT nextval('public.person_reader_id_seq'::regclass);


--
-- Name: publications lib_id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.publications ALTER COLUMN lib_id SET DEFAULT nextval('public.publications_lib_id_seq'::regclass);


--
-- Name: issue issue_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.issue
    ADD CONSTRAINT issue_pkey PRIMARY KEY (issue_id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (reader_id);


--
-- Name: publications publications_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.publications
    ADD CONSTRAINT publications_pkey PRIMARY KEY (lib_id);


--
-- Name: person unique_reader; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT unique_reader UNIQUE (full_name, id_card);


--
-- Name: issue isissued_false_ondelete_trigger; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER isissued_false_ondelete_trigger AFTER DELETE ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.change_issued_delete();


--
-- Name: issue isissued_false_trigger; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER isissued_false_trigger AFTER UPDATE OF returned_date ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.change_issued_return();


--
-- Name: issue isissued_trigger; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER isissued_trigger AFTER INSERT ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.change_issued();


--
-- Name: issue issue_when_not_issued; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER issue_when_not_issued BEFORE INSERT ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.issue_when_not_issued();


--
-- Name: issue set_delay; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER set_delay AFTER UPDATE OF returned_date ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.calculate_delay();


--
-- Name: issue sum_penalties_trigger; Type: TRIGGER; Schema: public; Owner: pi
--

CREATE TRIGGER sum_penalties_trigger AFTER UPDATE ON public.issue FOR EACH ROW EXECUTE PROCEDURE public.sum_penalties();


--
-- Name: issue issue_lib_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.issue
    ADD CONSTRAINT issue_lib_id_fkey FOREIGN KEY (lib_id) REFERENCES public.publications(lib_id);


--
-- Name: issue issue_reader_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.issue
    ADD CONSTRAINT issue_reader_id_fkey FOREIGN KEY (reader_id) REFERENCES public.person(reader_id);


--
-- PostgreSQL database dump complete
--

