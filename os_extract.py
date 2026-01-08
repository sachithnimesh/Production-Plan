import os
import xmlrpc.client
import pandas as pd
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# --- Authenticate ---
common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

if not uid:
    raise Exception("❌ Authentication failed. Check your .env values!")

print(f"✅ Authenticated successfully as UID {uid}")

# --- Access models ---
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# --- Get all fields from sale.report ---
fields = models.execute_kw(
    ODOO_DB, uid, ODOO_PASSWORD,
    'sale.report', 'fields_get',
    [], {'attributes': ['string']}
)

field_names = list(fields.keys())
print(f"🧩 Found {len(field_names)} fields in sale.report")

# --- Fetch all records (no row limit, in batches) ---
all_records = []
batch_size = 500
offset = 0

while True:
    batch = models.execute_kw(
        ODOO_DB, uid, ODOO_PASSWORD,
        'sale.report', 'search_read',
        [[]],
        {'fields': field_names, 'limit': batch_size, 'offset': offset, 'context': {'active_test': False}}
    )
    if not batch:
        break
    all_records.extend(batch)
    offset += batch_size
    print(f"  📦 Retrieved {len(batch)} records (Total so far: {len(all_records)})")

print(f"\n✅ Finished fetching {len(all_records)} records total")

# --- Convert to DataFrame ---
df = pd.DataFrame(all_records)

# --- Save to CSV ---
output_folder = "odoo_exports"
os.makedirs(output_folder, exist_ok=True)
csv_path = os.path.join(output_folder, "sale_report_full.csv")

df.to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"💾 Saved full sale.report data to: {csv_path}")

