import frappe

def execute():
    if frappe.db.exists("DocType", "Project Resource Plan"):
        return

    frappe.get_doc({
        "doctype": "DocType",
        "name": "Project Resource Plan",
        "module": "Fmg App",
        "istable": 1,
        "editable_grid": 1,
        "fields": [
            {
            'fieldname': 'custom_column_break_46f29',
            'label': '',
            'fieldtype': 'Column Break',
            'options': None,
            'insert_after': 'custom_labor_margin_type',
            "in_list_view": 1
            },
            {
            'fieldname': 'custom_section_break_lrlvs',
            'label': '',
            'fieldtype': 'Section Break',
            'options': None,
            'insert_after': 'total_rs',
            "in_list_view": 1
            }
        ]
    }).insert(ignore_permissions=True)
