import os
import json
import psycopg2

# Function to insert CVE details into the database
def insert_cve_details(cur, cve_item):
    # Extract necessary details from the CVE item
    cve_id = cve_item['cve']['CVE_data_meta']['ID']
    print(f"Inserting CVE details for: {cve_id}")
    data_type = cve_item['cve']['data_type']
    data_format = cve_item['cve']['data_format']
    data_version = cve_item['cve']['data_version']
    assigner = cve_item['cve']['CVE_data_meta']['ASSIGNER']
    published_date = cve_item.get('publishedDate', None)
    last_modified_date = cve_item.get('lastModifiedDate', None)
    
    # SQL command to insert the extracted data into the cve_details table
    cur.execute("""
    INSERT INTO cve_details (cve_id, data_type, data_format, data_version, assigner, published_date, last_modified_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (cve_id) DO NOTHING;
    """, (cve_id, data_type, data_format, data_version, assigner, published_date, last_modified_date))

# Function to insert problem types related to a CVE
def insert_problem_types(cur, cve_id, problem_types):
    print(f"Inserting problem types for: {cve_id}")
    for problem in problem_types['problemtype_data']:
        for description in problem['description']:
            # SQL command to insert problem types into the database
            cur.execute("""
                INSERT INTO problem_types (cve_id, description)
                VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (cve_id, json.dumps(description)))

# Function to insert references related to a CVE
def insert_references(cur, cve_id, references):
    print(f"Inserting references for: {cve_id}")
    for reference in references['reference_data']:
        # SQL command to insert references into the database
        cur.execute("""
            INSERT INTO cve_references (cve_id, url, name, refsource, tags)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """, (cve_id, reference['url'], reference['name'], reference['refsource'], json.dumps(reference.get('tags', []))))

# Function to insert descriptions related to a CVE
def insert_descriptions(cur, cve_id, descriptions):
    print(f"Inserting descriptions for: {cve_id}")
    for description in descriptions['description_data']:
        # SQL command to insert descriptions into the database
        cur.execute("""
            INSERT INTO descriptions (cve_id, lang, value)
            VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
        """, (cve_id, description['lang'], description['value']))

# Function to insert impact scores related to a CVE
def insert_impact(cur, cve_id, impact):
    print(f"Inserting impact for: {cve_id}")
    cvss_data = impact.get('baseMetricV3', {}).get('cvssV3', None) or impact.get('baseMetricV2', {}).get('cvssV2', None)
    if cvss_data:
        # SQL command to insert impact scores into the database
        cur.execute("""
            INSERT INTO impact (cve_id, cvss_data)
            VALUES (%s, %s) ON CONFLICT (cve_id) DO NOTHING;
        """, (cve_id, json.dumps(cvss_data)))

# Function to insert configurations related to a CVE
def insert_configurations(cur, cve_id, configurations):
    print(f"Inserting configurations for: {cve_id}")
    cve_data_version = configurations.get('CVE_data_version', '')
    nodes = configurations.get('nodes', [])
    # SQL command to insert configurations into the database
    cur.execute("""
        INSERT INTO configurations (cve_id, cve_data_version, nodes)
        VALUES (%s, %s, %s) ON CONFLICT (cve_id) DO NOTHING;
    """, (cve_id, cve_data_version, json.dumps(nodes)))

# Main function to process each JSON file in the specified directory
def process_file(filename, cur):
    print(f"Processing file: {filename}")
    with open(filename, 'r') as file:
        data = json.load(file)
        cve_items = data.get('CVE_Items', [])
        for cve_item in cve_items:
            # Process each CVE item by inserting its details into the database
            cve_id = cve_item['cve']['CVE_data_meta']['ID']
            insert_cve_details(cur, cve_item)
            insert_problem_types(cur, cve_id, cve_item['cve']['problemtype'])
            insert_references(cur, cve_id, cve_item['cve']['references'])
            insert_descriptions(cur, cve_id, cve_item['cve']['description'])
            insert_impact(cur, cve_id, cve_item.get('impact', {}))
            insert_configurations(cur, cve_id, cve_item.get('configurations', {}))

# Main entry point of the script
def main():
    directory = './nvd-data'
    # Establish database connection
    conn = psycopg2.connect(dbname="nvd", user="nvd-user", host="localhost")
    cur = conn.cursor()
    try:
        # Process each file in the directory
        for filename in os.listdir(directory):
            if filename.startswith("nvdcve-1.1") and filename.endswith(".json"):
                print(f"Processing {filename}")
                process_file(os.path.join(directory, filename), cur)
                conn.commit()  # Commit changes after each file is processed
                print(f"Finished processing and committed changes for {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
