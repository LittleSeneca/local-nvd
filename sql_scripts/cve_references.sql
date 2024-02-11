DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
        AND tablename = 'cve_references'
    ) THEN
    CREATE TABLE cve_references (
        reference_id SERIAL PRIMARY KEY,
        cve_id VARCHAR(50),
        url TEXT,
        name TEXT,
        refsource TEXT,
        tags JSONB,
        FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id)
    );
    END IF;
END
$$;