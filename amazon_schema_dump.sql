--
-- PostgreSQL database dump
--

-- Dumped from database version 13.13 (Debian 13.13-0+deb11u1)
-- Dumped by pg_dump version 13.13 (Debian 13.13-0+deb11u1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: attributes; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.attributes (
    id integer NOT NULL,
    name text NOT NULL,
    value text NOT NULL,
    element_id integer
);


ALTER TABLE public.attributes OWNER TO micheldc;

--
-- Name: attributes_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

ALTER TABLE public.attributes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.attributes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: elements; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.elements (
    id integer NOT NULL,
    type text,
    topics double precision[],
    tags text[],
    sentiments integer[],
    item_id integer,
    text text,
    summary text,
    rating double precision,
    attributes json
);


ALTER TABLE public.elements OWNER TO micheldc;

--
-- Name: elements_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

ALTER TABLE public.elements ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.elements_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: exploration_iteration; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.exploration_iteration (
    id integer NOT NULL,
    session_name text,
    iteration integer,
    feedback integer,
    guidance integer[],
    terminate boolean
);


ALTER TABLE public.exploration_iteration OWNER TO micheldc;

--
-- Name: exploration_iteration_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

CREATE SEQUENCE public.exploration_iteration_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exploration_iteration_id_seq OWNER TO micheldc;

--
-- Name: exploration_iteration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: micheldc
--

ALTER SEQUENCE public.exploration_iteration_id_seq OWNED BY public.exploration_iteration.id;


--
-- Name: items; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.items (
    id integer NOT NULL,
    asin text,
    price text,
    title text,
    also_view jsonb,
    also_buy jsonb,
    rank jsonb,
    category jsonb,
    description text,
    image text,
    feature jsonb,
    main_cat text,
    similar_item text,
    date text
);


ALTER TABLE public.items OWNER TO micheldc;

--
-- Name: meta_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

CREATE SEQUENCE public.meta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meta_id_seq OWNER TO micheldc;

--
-- Name: meta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: micheldc
--

ALTER SEQUENCE public.meta_id_seq OWNED BY public.items.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    asin text,
    helpful_true integer,
    overall numeric,
    summary text,
    reviewtext text,
    reviewtime text,
    reviewerid text,
    reviewername text,
    unixreviewtime text,
    helpful_all integer,
    in_sample boolean
);


ALTER TABLE public.reviews OWNER TO micheldc;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO micheldc;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: micheldc
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: session; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.session (
    id integer NOT NULL,
    name text,
    iterations_so_far text,
    target text
);


ALTER TABLE public.session OWNER TO micheldc;

--
-- Name: session_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

CREATE SEQUENCE public.session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.session_id_seq OWNER TO micheldc;

--
-- Name: session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: micheldc
--

ALTER SEQUENCE public.session_id_seq OWNED BY public.session.id;


--
-- Name: similarities; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.similarities (
    id integer NOT NULL,
    sim double precision,
    sentiment_sim double precision,
    tag_sim double precision,
    topic_sim double precision,
    attribute_sim double precision,
    element1_id integer NOT NULL,
    element2_id integer NOT NULL,
    summary_sim double precision
);


ALTER TABLE public.similarities OWNER TO micheldc;

--
-- Name: similarities_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

ALTER TABLE public.similarities ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.similarities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: topic_definition; Type: TABLE; Schema: public; Owner: micheldc
--

CREATE TABLE public.topic_definition (
    id integer NOT NULL,
    words text,
    topic_id integer
);


ALTER TABLE public.topic_definition OWNER TO micheldc;

--
-- Name: topic_definition_id_seq; Type: SEQUENCE; Schema: public; Owner: micheldc
--

CREATE SEQUENCE public.topic_definition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.topic_definition_id_seq OWNER TO micheldc;

--
-- Name: topic_definition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: micheldc
--

ALTER SEQUENCE public.topic_definition_id_seq OWNED BY public.topic_definition.id;


--
-- Name: exploration_iteration id; Type: DEFAULT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.exploration_iteration ALTER COLUMN id SET DEFAULT nextval('public.exploration_iteration_id_seq'::regclass);


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.meta_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: session id; Type: DEFAULT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.session ALTER COLUMN id SET DEFAULT nextval('public.session_id_seq'::regclass);


--
-- Name: topic_definition id; Type: DEFAULT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.topic_definition ALTER COLUMN id SET DEFAULT nextval('public.topic_definition_id_seq'::regclass);


--
-- Name: items asin_unique; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT asin_unique UNIQUE (asin);


--
-- Name: attributes attributes_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT attributes_pkey PRIMARY KEY (id);


--
-- Name: elements elements_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.elements
    ADD CONSTRAINT elements_pkey PRIMARY KEY (id);


--
-- Name: exploration_iteration exploration_iteration_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.exploration_iteration
    ADD CONSTRAINT exploration_iteration_pkey PRIMARY KEY (id);


--
-- Name: items meta_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT meta_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: session session_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pkey PRIMARY KEY (id);


--
-- Name: similarities similarities_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.similarities
    ADD CONSTRAINT similarities_pkey PRIMARY KEY (id);


--
-- Name: topic_definition topic_definition_pkey; Type: CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.topic_definition
    ADD CONSTRAINT topic_definition_pkey PRIMARY KEY (id);


--
-- Name: fki_attribute_element_fkey; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX fki_attribute_element_fkey ON public.attributes USING btree (element_id);


--
-- Name: fki_element_review_item_fkey; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX fki_element_review_item_fkey ON public.elements USING btree (item_id);


--
-- Name: fki_sim_element1_fkey; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX fki_sim_element1_fkey ON public.similarities USING btree (element1_id);


--
-- Name: fki_sim_element2_fkey; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX fki_sim_element2_fkey ON public.similarities USING btree (element2_id);


--
-- Name: meta_asin_idx; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX meta_asin_idx ON public.items USING btree (asin);


--
-- Name: reviews_asin_idx; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX reviews_asin_idx ON public.reviews USING btree (asin);


--
-- Name: reviews_id_idx; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX reviews_id_idx ON public.reviews USING btree (id);


--
-- Name: reviews_in_sample_idx; Type: INDEX; Schema: public; Owner: micheldc
--

CREATE INDEX reviews_in_sample_idx ON public.reviews USING btree (in_sample);


--
-- Name: attributes attribute_element_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT attribute_element_fkey FOREIGN KEY (element_id) REFERENCES public.elements(id);


--
-- Name: attributes element_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT element_fkey FOREIGN KEY (element_id) REFERENCES public.elements(id);


--
-- Name: elements element_review_item_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.elements
    ADD CONSTRAINT element_review_item_fkey FOREIGN KEY (item_id) REFERENCES public.elements(id);


--
-- Name: reviews items_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT items_fkey FOREIGN KEY (asin) REFERENCES public.items(asin);


--
-- Name: similarities sim_element1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.similarities
    ADD CONSTRAINT sim_element1_fkey FOREIGN KEY (element1_id) REFERENCES public.elements(id);


--
-- Name: similarities sim_element2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: micheldc
--

ALTER TABLE ONLY public.similarities
    ADD CONSTRAINT sim_element2_fkey FOREIGN KEY (element2_id) REFERENCES public.elements(id);


--
-- PostgreSQL database dump complete
--

