
# Production Planning & Analytics – Project Flow

## Overview
This project automates **data extraction, analysis, and production planning** using:

- **Odoo** as the source system  
- **Python ETL scripts**
- **Power BI** for store balance and production time analysis  
- **OpenAI (ChatGPT UI)** for intelligent production plan generation  

The objective is to transform operational data into **accurate, capacity-based weekly production plans**.

---

## Repository Structure

```text
src/
├── .env
├── .gitignore
├── csv_extract.py
├── os_extract.py
├── project_flow.md
└── README.md
````

---

## System Architecture

<!-- INSERT FLOWCHART IMAGE BELOW -->

<!-- Recommended path: docs/images/production_flowchart.png -->

![Production Flowchart](https://github.com/sachithnimesh/Production-Plan/blob/main/src/Flow%20chart.png?raw=true)

---

## End-to-End Workflow

### Step 1: Data Source – Odoo Database

Odoo acts as the **single source of truth** and contains:

* Sales Orders (OS Number)
* Customer information
* Product details
* Ordered quantities
* Store balances
* Production master data

---

### Step 2: OS Data Extraction (`os_extract.py`)

**Purpose:** Extract sales order and production-related data from Odoo.

**Responsibilities:**

* Load credentials from `.env`
* Connect to Odoo (API / database)
* Extract:

  * OS Number
  * Customer
  * Product
  * Quantity
* Clean and standardize data

**Output:**

* Structured data passed to CSV generation

---

### Step 3: CSV Generation (`csv_extract.py`)

**Purpose:** Convert extracted data into analysis-ready CSV files.

**Responsibilities:**

* Apply business rules
* Normalize quantities and units
* Generate clean CSV outputs
* Ensure compatibility with:

  * Power BI
  * OpenAI (ChatGPT UI)

**Output:**

* CSV files as a shared data layer

---

## Decision Layer

After CSV generation, data is routed based on business requirements:

| Requirement                | Tool                |
| -------------------------- | ------------------- |
| Store balance checking     | Power BI            |
| Production time analysis   | Power BI            |
| Weekly production planning | OpenAI (ChatGPT UI) |

---

## Power BI Workflow

### Step 4: Inventory & Production Analysis

Power BI uses the CSV files to:

* Monitor store-wise inventory
* Track open OS orders
* Analyze production time per product
* Identify shortages and capacity constraints

**Outputs:**

* Interactive dashboards
* Filtered analytical views
* Decision-support insights

---

## OpenAI (ChatGPT UI) Workflow

### Step 5: AI-Assisted Production Planning

OpenAI (ChatGPT UI) is used to generate **weekly production plans**.

**Inputs to ChatGPT:**

* OS report (CSV)
* Production time sheet
* Workforce constraints:

  * 20 workers
  * 11 hours per day
  * 5 working days per week

**AI Responsibilities:**

* Allocate production into time slots
* Balance manpower capacity
* Prevent over- or under-utilization
* Generate factory-style production schedules

**Outputs:**

* Weekly production plan
* Excel-style layout
* Ready for shop-floor execution

---

## Configuration

### Environment Variables (`.env`)

Used to store:

* Odoo credentials
* Database connection details

> `.env` is excluded from Git via `.gitignore`

---

## Key Benefits

* Automated ETL process
* Single CSV-based data layer
* Visual insights with Power BI
* AI-driven production planning
* Reduced manual errors
* Improved resource utilization
* Automated Power BI refresh


---


