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
-- Data for Name: issue; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY public.issue (issue_id, lib_id, reader_id, issue_date, issue_limit, returned_date, delay, imposed_penalty) FROM stdin;
112	26	24	2021-05-30	2021-06-29	\N	\N	\N
\.


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY public.person (reader_id, full_name, phone_number, email, id_card, total_penalty) FROM stdin;
18	Findley Lawson	354-942-1461	\N	375-11-7200	6.60
20	Rodolphe Peel	540-245-5816	rpeelj@behance.net	287-93-5601	6.60
22	Birk Blakemore	402-189-6124	\N	233-22-0581	6.60
25	Vitia Summerton	693-753-7690	\N	632-07-1427	6.60
21	Jammie Leidecker	160-771-8004	jleideckerk@imageshack.us	366-60-4083	6.60
23	Chariot Korting	896-628-8531	ckortingm@typepad.com	411-27-5352	6.60
24	Lesli Sirmon	943-623-2169	lsirmonn@smh.com.au	348-03-0863	6.60
17	Almire Van Velden	160-624-0560	avang@eventbrite.com	641-14-4178	6.60
1	Lauryn McEntagart	129-145-5437	lmcentagart0@kickstarter.com	254-22-1526	6.60
2	Karilynn Blything	768-427-1648	kblything1@spiegel.de	581-89-0894	6.60
3	Cordy McCormack	512-129-6591	cmccormack2@howstuffworks.com	694-78-7010	6.60
4	Kimbra Proctor	\N	\N	347-19-2138	6.60
5	Bekki Alywin	\N	balywin4@plala.or.jp	190-70-2328	6.60
6	Bobette Lerner	600-511-8151	blerner5@noaa.gov	212-47-0411	6.60
7	Jermaine Fickling	595-219-8247	\N	775-14-4917	6.60
8	Mariana Meekins	225-364-1581	mmeekins7@usda.gov	273-31-8550	6.60
9	Ingeborg Guterson	611-913-7297	iguterson8@xinhuanet.com	801-67-8308	6.60
10	Elisha Benford	326-167-2068	\N	223-45-2831	6.60
11	Burl Allerton	841-637-2660	\N	785-36-4153	6.60
12	Briano Gapper	394-907-1661	bgapperb@irs.gov	276-22-9824	6.60
13	Britni Dimic	585-509-2812	bdimicc@noaa.gov	344-02-4551	6.60
19	Pierette McComb	135-927-1543	\N	797-47-9297	6.60
26	Gaultiero Eyrl	288-851-9842	geyrlp@jimdo.com	238-54-4714	6.60
27	Carissa Cordier	803-647-4337	ccordierq@reverbnation.com	775-21-8703	6.60
28	Caroljean Thew	\N	cthewr@cdbaby.com	431-49-8544	6.60
29	Thain Goodinson	969-582-2231	tgoodinsons@mtv.com	224-13-4529	6.60
30	Chelsey Corrison	942-396-0395	ccorrisont@163.com	871-49-9389	6.60
16	Serene Tortoishell	336-909-1202	\N	188-09-6337	6.60
14	Shina Cotterell	706-415-9148	scotterelld@ycombinator.com	590-66-9478	6.60
15	Manon Mattia	734-178-4241	\N	707-89-5724	6.60
\.


--
-- Data for Name: publications; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY public.publications (lib_id, title, author, kind, publisher, year_of_publish, language, pages, isbn, is_issued) FROM stdin;
3	Hand That Rocks the Cradle, The	Sherri Biddwell	Drama|Thriller	Sage	1995	Quechua	210	779914925-6	f
5	Bigfoot Lives	Hermy Ashbe	Adventure|Documentary|Drama	Dryden	2000	Albanian	306	694852980-1	f
33	Mike Tyson:  Undisputed Truth	Demetria Wardrop	Comedy	John Wall	1996	Croatian	\N	770452933-1	f
26	Blood of the Beasts (Sang des bêtes, Le)	Catarina Storcke	Documentary|Drama	Vernon	1995	Persian	391	713547340-X	t
13	Nightmare on Elm Street 3: Dream Warriors, A	Orland Puvia	Horror|Thriller	Dorton	2001	Tsonga	88	676120409-7	f
14	Last Hurrah, The	Yolanda Mawby	Drama	Linden	1986	Guaraní	305	624166103-5	f
16	Macbeth in Manhattan	Mikaela Smithen	\N	Forster	2000	Macedonian	302	\N	f
19	Hell's Hinges	Boris Hannaford	\N	Caliangt	2011	Guaraní	213	\N	f
21	Tom at the Farm (Tom à la ferme)	Jim Jenson	Drama	Golden Leaf	2000	Icelandic	\N	008031045-1	f
22	Jim Jefferies: BARE	Shandra Jamot	Comedy	Jana	1987	Danish	\N	066695296-5	f
27	Private Affairs of Bel Ami, The	Myriam Barnham	Drama	Esker	1962	Bulgarian	273	151061716-7	f
28	Ski Patrol	Walliw Besson	Action|War	Manufacturers	1997	Somali	159	162410320-0	f
29	Raze	Jelene Paulat	Action|Horror	Shasta	2006	Estonian	375	013465005-0	f
30	Better Than Chocolate	Dorothea Goddard	Comedy|Romance	Clyde Gallagher	1992	Lithuanian	217	119451217-8	f
31	Money Train	Pierrette Hulburt	Action|Comedy|Crime|Drama|Thriller	Ohio	2011	Filipino	117	377907642-X	f
32	Lonesome Dove	Ema Hadden	Adventure|Drama|Western	Spohn	1998	Gujarati	357	218899242-3	f
37	Germinal	Reba Shakelady	Drama|Romance	Northwestern	2007	Czech	277	532425265-4	f
38	Jacques Brel Is Alive and Well and Living in Paris	Courtnay Antyshev	Musical	Gerald	1990	Hiri Motu	255	192241485-9	f
39	Beyond Borders	Sauncho Razoux	Drama|Romance|War	Pennsylvania	2010	Malayalam	351	929334700-8	f
40	City Streets	Allison Highway	Crime|Film-Noir	Red Cloud	2007	Burmese	153	115348574-5	f
34	Oscar	Carolynn Hardan	Comedy|Crime|Mystery|Romance	Hoepker	2005	Chinese	344	775698909-0	f
24	Photographing Fairies	Stavro Denyer	Drama|Fantasy|Mystery	Ridgeview	1992	Fijian	399	738116553-8	f
25	Because You're Mine	Paule Bernhardt	Comedy|Musical	Marquette	2012	Afrikaans	396	509677913-0	f
4	Song for Martin, A (Sång för Martin, En)	Dixie Bulstrode	\N	Eastwood	2008	German	367	\N	f
8	Closely Watched Trains (Ostre sledované vlaky)	Gretel Ruthven	Comedy|Drama|War	Claremont	2005	Macedonian	\N	314409127-8	f
17	Take This Job and Shove It	Caitlin Froom	Comedy	Hauk	1997	Spanish	86	948618597-2	f
18	America's Heart and Soul	Lenka Sandison	Documentary	Katie	1995	Italian	339	209708208-4	f
35	Deep Cover	Francine Henrichsen	Action|Crime|Thriller	Elka	2010	Punjabi	212	065311863-5	f
9	Shatter Dead	Lorne Tankard	Horror	Morrow	1996	Catalan	\N	889317099-X	f
20	Simpsons: The Longest Daycare, The	Clementina Bucklee	\N	Steensland	1972	Gagauz	91	\N	f
11	Blue Collar	Linea Maciaszczyk	Crime|Drama	Charing Cross	2010	Chinese	243	611434658-0	f
\.


--
-- Name: issue_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('public.issue_issue_id_seq', 112, true);


--
-- Name: person_reader_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('public.person_reader_id_seq', 192, true);


--
-- Name: publications_lib_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('public.publications_lib_id_seq', 1048, true);


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

