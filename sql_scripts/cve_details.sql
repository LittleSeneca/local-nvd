DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_tables
        WHERE schemaname = 'public'
        AND tablename = 'cve_details'
    ) THEN
    CREATE TABLE cve_details (
        cve_id VARCHAR(50) PRIMARY KEY,
        data_type VARCHAR(10),
        data_format VARCHAR(10),
        data_version VARCHAR(10),
        assigner VARCHAR(255),
        published_date TIMESTAMP WITH TIME ZONE,
        last_modified_date TIMESTAMP WITH TIME ZONE
    );
    END IF;
END
$$;