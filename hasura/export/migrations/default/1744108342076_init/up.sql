SET transaction_timeout = 0;
SET check_function_bodies = false;
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;
COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';
CREATE TYPE public.subscription_enum AS ENUM (
    'updates',
    'tags',
    'creates'
);
CREATE FUNCTION public.set_current_timestamp_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
  _new record;
BEGIN
  _new := NEW;
  _new."updated_at" = NOW();
  RETURN _new;
END;
$$;
CREATE TABLE public.entries (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    id text NOT NULL,
    status text NOT NULL,
    lat numeric NOT NULL,
    lng numeric NOT NULL,
    title text NOT NULL,
    description text NOT NULL
);
CREATE TABLE public.entry_categories (
    entry text NOT NULL,
    category text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);
CREATE TABLE public.entry_links (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    entry text NOT NULL,
    link integer NOT NULL
);
CREATE TABLE public.entry_tags (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    entry text NOT NULL,
    tag text NOT NULL
);
CREATE TABLE public.link (
    id integer NOT NULL,
    url text NOT NULL,
    title text,
    description text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);
CREATE SEQUENCE public.link_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.link_id_seq OWNED BY public.link.id;
CREATE TABLE public.subscriptions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email text NOT NULL,
    lat_min numeric NOT NULL,
    lon_min numeric NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    n_emails_sent integer DEFAULT 0 NOT NULL,
    "interval" text NOT NULL,
    lat_max numeric NOT NULL,
    lon_max numeric NOT NULL,
    last_email_sent_at timestamp with time zone,
    subscription_type public.subscription_enum NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    language text DEFAULT 'de'::text,
    title text NOT NULL
);
CREATE TABLE public.tags (
    id text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);
ALTER TABLE ONLY public.link ALTER COLUMN id SET DEFAULT nextval('public.link_id_seq'::regclass);
ALTER TABLE ONLY public.entries
    ADD CONSTRAINT entries_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.entry_categories
    ADD CONSTRAINT entry_categories_pkey PRIMARY KEY (entry, category);
ALTER TABLE ONLY public.entry_links
    ADD CONSTRAINT entry_links_pkey PRIMARY KEY (entry, link);
ALTER TABLE ONLY public.entry_tags
    ADD CONSTRAINT entry_tags_pkey PRIMARY KEY (entry, tag);
ALTER TABLE ONLY public.link
    ADD CONSTRAINT link_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.subscriptions
    ADD CONSTRAINT subscribers_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);
CREATE TRIGGER set_public_entries_updated_at BEFORE UPDATE ON public.entries FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_entries_updated_at ON public.entries IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_link_updated_at BEFORE UPDATE ON public.link FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_link_updated_at ON public.link IS 'trigger to set value of column "updated_at" to current timestamp on row update';
CREATE TRIGGER set_public_subscribers_updated_at BEFORE UPDATE ON public.subscriptions FOR EACH ROW EXECUTE FUNCTION public.set_current_timestamp_updated_at();
COMMENT ON TRIGGER set_public_subscribers_updated_at ON public.subscriptions IS 'trigger to set value of column "updated_at" to current timestamp on row update';
ALTER TABLE ONLY public.entry_categories
    ADD CONSTRAINT entry_categories_entry_fkey FOREIGN KEY (entry) REFERENCES public.entries(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.entry_links
    ADD CONSTRAINT entry_links_entry_fkey FOREIGN KEY (entry) REFERENCES public.entries(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.entry_links
    ADD CONSTRAINT entry_links_link_fkey FOREIGN KEY (link) REFERENCES public.link(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.entry_tags
    ADD CONSTRAINT entry_tags_entry_fkey FOREIGN KEY (entry) REFERENCES public.entries(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
ALTER TABLE ONLY public.entry_tags
    ADD CONSTRAINT entry_tags_tag_fkey FOREIGN KEY (tag) REFERENCES public.tags(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
