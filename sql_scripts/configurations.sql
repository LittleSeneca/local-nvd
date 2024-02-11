CREATE TABLE configurations (
    configuration_id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50),
    cve_data_version VARCHAR(10),
    nodes JSONB,
    FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id)
    UNIQUE (cve_id)
);