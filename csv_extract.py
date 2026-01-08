
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
    raise Exception("❌ Authentication failed")

print(f"✅ Authenticated as UID {uid}")

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

EXPORT_FOLDER = "odoo_exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

# TARGET_MODELS = [
#     "account.analytic.line",
#     "mrp.bom",
#     "mrp.bom.line",
#     "stock.move",
# ]
TARGET_MODELS = [
    "mrp.bom",
    "mrp.bom.line",
    "stock.move",
    "sale.order",          
]

BATCH_SIZE = 1000

for model_name in TARGET_MODELS:
    print(f"\n📤 Exporting {model_name} ...")

    try:
        ids = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            model_name, 'search',
            [[]],
            {'context': {'active_test': False}}
        )

        if not ids:
            print("  ⚠️ No data found")
            continue

        all_records = []

        for i in range(0, len(ids), BATCH_SIZE):
            batch_ids = ids[i:i + BATCH_SIZE]
            records = models.execute_kw(
                ODOO_DB, uid, ODOO_PASSWORD,
                model_name, 'read',
                [batch_ids],
                {'context': {'active_test': False}}
            )
            all_records.extend(records)

        df = pd.DataFrame(all_records)

        # 🔥 SPECIAL LOGIC FOR mrp.bom
        if model_name == "mrp.bom":
            print("  🔄 Ungrouping bom_line_ids")

            if "bom_line_ids" in df.columns:
                df = df.explode("bom_line_ids")
                df = df.rename(columns={"bom_line_ids": "bom_line_id"})

        csv_path = os.path.join(
            EXPORT_FOLDER,
            f"{model_name.replace('.', '_')}.csv"
        )

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"  ✅ Saved {len(df)} rows → {csv_path}")

    except Exception as e:
        print(f"  ❌ Error exporting {model_name}: {e}")

print("\n🎉 Export completed with BOM lines normalized.")
