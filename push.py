import os
import json
import psycopg2

def insert_cve_details(cur, cve_item):
    cve_id = cve_item['cve']['CVE_data_meta']['ID']
    data_type = cve_item['cve']['data_type']
    data_format = cve_item['cve']['data_format']
    data_version = cve_item['cve']['data_version']
    assigner = cve_item['cve']['CVE_data_meta']['ASSIGNER']
    published_date = cve_item.get('publishedDate', None)
    last_modified_date = cve_item.get('lastModifiedDate', None)
    
    cur.execute("""
    INSERT INTO cve_details (cve_id, data_type, data_format, data_version, assigner, published_date, last_modified_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (cve_id) DO NOTHING;
    """, (cve_id, data_type, data_format, data_version, assigner, published_date, last_modified_date))

def insert_problem_types(cur, cve_id, problem_types):
    for problem in problem_types['problemtype_data']:
        for description in problem['description']:
            cur.execute("""
                INSERT INTO problem_types (cve_id, description)
                VALUES (%s, %s) ON CONFLICT DO NOTHING;
            """, (cve_id, json.dumps(description)))

def insert_references(cur, cve_id, references):
    for reference in references['reference_data']:
        cur.execute("""
            INSERT INTO cve_references (cve_id, url, name, refsource, tags)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """, (cve_id, reference['url'], reference['name'], reference['refsource'], json.dumps(reference.get('tags', []))))

def insert_descriptions(cur, cve_id, descriptions):
    for description in descriptions['description_data']:
        cur.execute("""
            INSERT INTO descriptions (cve_id, lang, value)
            VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
        """, (cve_id, description['lang'], description['value']))

def insert_impact(cur, cve_id, impact):
    cvss_data = impact.get('baseMetricV3', {}).get('cvssV3', None) or impact.get('baseMetricV2', {}).get('cvssV2', None)
    if cvss_data:
        cur.execute("""
            INSERT INTO impact (cve_id, cvss_data)
            VALUES (%s, %s) ON CONFLICT (cve_id) DO NOTHING;
        """, (cve_id, json.dumps(cvss_data)))

def insert_configurations(cur, cve_id, configurations):
    cve_data_version = configurations.get('CVE_data_version', '')
    nodes = configurations.get('nodes', [])
    cur.execute("""
        INSERT INTO configurations (cve_id, cve_data_version, nodes)
        VALUES (%s, %s, %s) ON CONFLICT (cve_id) DO NOTHING;
    """, (cve_id, cve_data_version, json.dumps(nodes)))

def process_file(filename, cur):
    print(f"Processing file: {filename}")
    with open(filename, 'r') as file:
        data = json.load(file)
        cve_items = data.get('CVE_Items', [])
        for cve_item in cve_items:
            cve_id = cve_item['cve']['CVE_data_meta']['ID']
            insert_cve_details(cur, cve_item)
            insert_problem_types(cur, cve_id, cve_item['cve']['problemtype'])
            insert_references(cur, cve_id, cve_item['cve']['references'])
            insert_descriptions(cur, cve_id, cve_item['cve']['description'])
            insert_impact(cur, cve_id, cve_item.get('impact', {}))
            insert_configurations(cur, cve_id, cve_item.get('configurations', {}))

def main():
    directory = './nvd-data'
    conn = psycopg2.connect(dbname="nvd", user="nvd-user", password="your_password", host="localhost")
    cur = conn.cursor()
    try:
        for filename in os.listdir(directory):
            if filename.startswith("nvdcve-1.1") and filename.endswith(".json"):
                process_file(os.path.join(directory, filename), cur)
                conn.commit()
                print(f"Finished processing and committed changes for {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
