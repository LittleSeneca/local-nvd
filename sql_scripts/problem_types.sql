DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
        AND tablename = 'problem_types'
    ) THEN
    CREATE TABLE problem_types (
        problem_type_id SERIAL PRIMARY KEY,
        cve_id VARCHAR(50),
        description JSONB,
        FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id)
    );
    END IF;
END
$$;