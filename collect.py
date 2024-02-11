import os
from datetime import datetime
import http.client

os.system('mkdir ./nvd-data')
currentYear = datetime.now().year

for year in range(2002, currentYear):
    conn = http.client.HTTPSConnection("nvd.nist.gov")
    conn.request("GET", f"/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz")
    res = conn.getresponse()
    if res.status == 200:
        if not os.path.exists(f'./nvd-data/nvdcve-1.1-{year}.json.gz'):
            os.system(f'wget -P ./nvd-data https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz')
        else:
            print(f"File already exists for year: {year}")
    else:
        print(f"Failed to download file for year: {year}")

for year in range(2002, currentYear):
    if os.path.exists(f'./nvd-data/nvdcve-1.1-{year}.json.gz'):
        os.system(f'gunzip ./nvd-data/nvdcve-1.1-{year}.json.gz')
    elif os.path.exists(f'./nvd-data/nvdcve-1.1-{year}.json'):
        print(f"File already unzipped for year: {year}")