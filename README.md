# Production Plan - Odoo Export for Business Reporting

This project exports operational data from Odoo into CSV files used for production
planning and reporting (e.g., Power BI). It targets sales, BOM, and stock data so
business users can analyze demand, capacity, and material requirements from a
single, refreshable dataset.

## Business use case
- Align production planning with current sales demand and confirmed orders.
- Break down BOM structures to understand material needs by product.
- Track stock movements to validate availability and lead-time risk.
- Refresh reporting outputs without manual exports from Odoo.

## What it does
- Pulls data from Odoo via XML-RPC.
- Exports CSVs into `odoo_exports/` for reporting tools.
- Includes a separate extractor for the full `sale.report` model.

## Data outputs (typical)
- `odoo_exports/mrp_bom.csv`
- `odoo_exports/mrp_bom_line.csv`
- `odoo_exports/stock_move.csv`
- `odoo_exports/sale_order.csv`
- `odoo_exports/sale_report_full.csv`

## Requirements
- Python 3.9+ (recommended)
- `pandas`
- `python-dotenv`

Install dependencies:
```bash
pip install pandas python-dotenv
```

## Configuration
Create a `.env` file in the project root with your Odoo connection values:
```
ODOO_URL=https://your-odoo.example.com
ODOO_DB=your_db
ODOO_USERNAME=your_user
ODOO_PASSWORD=your_password
```

## Usage
Export core production data:
```bash
python csv_extract.py
```

Export full sales reporting dataset:
```bash
python os_extract.py
```

## Notes
- CSVs are written to `odoo_exports/` (created if missing).
- Large datasets are fetched in batches to reduce memory pressure.
- Keep credentials in `.env`; avoid committing it to version control.

## Suggested workflow
1) Run the extractors on a schedule (manual or task scheduler).
2) Refresh the Power BI report (`odoo_exports/Production Plan.pbix`).
3) Validate outputs against expected row counts in Odoo.

