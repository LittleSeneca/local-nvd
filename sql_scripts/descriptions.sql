CREATE TABLE descriptions (
    description_id SERIAL PRIMARY KEY,
    cve_id VARCHAR(50),
    lang VARCHAR(5),
    value TEXT,
    FOREIGN KEY (cve_id) REFERENCES cve_details(cve_id)
    UNIQUE (cve_id)
);