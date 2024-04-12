# Copyright (c) 2024, vedika and contributors
# For license information, please see license.txt
import frappe
def create_index(index_name, sql_query):
    try:
        frappe.db.sql(sql_query)
        print(f"Index {index_name} created successfully.")
    except Exception as e:
        if "Duplicate key name" in str(e):
            print(f"Index {index_name} already exists.")
        else:
            print(f"Error creating index {index_name}: {e}")
index_queries = [
    ("idx_warehouse_item_code", "CREATE INDEX idx_warehouse_item_code ON `tabBin` (warehouse, item_code)"),
    ("idx_reserved_qty_for_production", "CREATE INDEX idx_reserved_qty_for_production ON `tabBin` (reserved_qty_for_production)"),
    ("idx_actual_qty", "CREATE INDEX idx_actual_qty ON `tabBin` (actual_qty)")
]

for index_name, query in index_queries:
    create_index(index_name, query)
def execute(filters=None):
    columns = [
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Reserved Qty for Production", "fieldname": "reserved_qty_for_production", "fieldtype": "Float"},
        {"label": "Actual Qty", "fieldname": "actual_qty", "fieldtype": "Float"},
        {"label": "Valuation Rate", "fieldname": "valuation_rate", "fieldtype": "Currency"}
    ]
    data = []
    warehouse_filter = filters.get('warehouse')
    filter_clause = ""
    if warehouse_filter:
        filter_clause = f"WHERE bin.warehouse = '{warehouse_filter}'"
    
    sql_query = f"""
        SELECT
            bin.warehouse,
            bin.item_code,
            bin.reserved_qty_for_production,
            bin.actual_qty,
            bin.valuation_rate
        FROM
            `tabBin` bin
        {filter_clause}
        ORDER BY
            bin.warehouse,
            bin.item_code
    """
    stock_entries = frappe.db.sql(sql_query, as_dict=True)
    for row in stock_entries:
        data.append(row)
    return columns, data
