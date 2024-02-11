CREATE TABLE impact (
    impact_id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50),
    cvss_data JSONB,
    FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id)
);