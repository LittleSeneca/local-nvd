DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
        AND tablename = 'descriptions'
    ) THEN
    CREATE TABLE descriptions (
        description_id SERIAL PRIMARY KEY,
        cve_id VARCHAR(50),
        lang VARCHAR(5),
        value TEXT,
        FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id),
        UNIQUE (cve_id)
    );
    END IF;
END
$$;