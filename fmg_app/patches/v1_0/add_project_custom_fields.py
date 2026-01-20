import frappe

def execute():
    # Safety: sirf tab chale jab FMG installed ho
    if "fmg_app" not in frappe.get_installed_apps():
        return

    fields = [
        {
            "dt": "Project",
            "fieldname": "custom_project_planning",
            "label": "Project Planning",
            "fieldtype": "Section Break",
            "insert_after": None
        },
        {
            "dt": "Project",
            "fieldname": "custom_company_copy",
            "label": "Company Name",
            "fieldtype": "Link",
            "options": "Company",
            "insert_after": "custom_project_planning"
        },
        {
            "dt": "Project",
            "fieldname": "custom_column_break_osfbk",
            "label": "",
            "fieldtype": "Column Break",
            "insert_after": "custom_company_copy"
        },
        {
            "dt": "Project",
            "fieldname": "custom_type_of_flooring",
            "label": "Flooring Type",
            "fieldtype": "Link",
            "options": "Item",
            "insert_after": "custom_column_break_osfbk"
        },
        {
            "dt": "Project",
            "fieldname": "custom_section_break_nf0xo",
            "label": "",
            "fieldtype": "Section Break",
            "insert_after": "custom_type_of_flooring"
        },
        {
            "dt": "Project",
            "fieldname": "custom_warehouse_area",
            "label": "Flooring Area",
            "fieldtype": "Float",
            "insert_after": "custom_section_break_nf0xo"
        },
        {
            "dt": "Project",
            "fieldname": "custom_floor_thickness",
            "label": "Floor Thickness",
            "fieldtype": "Float",
            "insert_after": "custom_warehouse_area"
        },
        {
            "dt": "Project",
            "fieldname": "custom_column_break_es2na",
            "label": "",
            "fieldtype": "Column Break",
            "insert_after": "custom_floor_thickness"
        },
        {
            "dt": "Project",
            "fieldname": "custom_new_uom",
            "label": "UOM",
            "fieldtype": "Select",
            "options": "Square Meter",
            "insert_after": "custom_column_break_es2na"
        },
        {
            "dt": "Project",
            "fieldname": "custom_new_uom_thickness",
            "label": "UOM (Thickness)",
            "fieldtype": "Select",
            "options": "Meter",
            "insert_after": "custom_new_uom"
        },
        {
            "dt": "Project",
            "fieldname": "custom_uom",
            "label": "UOM",
            "fieldtype": "Link",
            "options": "UOM",
            "insert_after": "custom_new_uom_thickness"
        },
        {
            "dt": "Project",
            "fieldname": "custom_uom_thickness",
            "label": "UOM (Thickness)",
            "fieldtype": "Link",
            "options": "UOM",
            "insert_after": "custom_uom"
        },
        {
            "dt": "Project",
            "fieldname": "custom_section_break_iw3fy",
            "label": "Project Resource Plan",
            "fieldtype": "Section Break",
            "insert_after": "custom_uom_thickness"
        },
        {
            "dt": "Project",
            "fieldname": "custom_requirements",
            "label": "Requirements",
            "fieldtype": "Section Break",
            "insert_after": "custom_site_incharge"
        },
        {
            "dt": "Project",
            "fieldname": "custom_project_cost_summary",
            "label": "Project Cost Summary",
            "fieldtype": "Section Break",
            "insert_after": "custom_material_coverage_details"
        },
        {
            "dt": "Project",
            "fieldname": "custom_total_project_material_",
            "label": "Total Project Material (₹)",
            "fieldtype": "Currency",
            "insert_after": "custom_project_cost_summary"
        },
        {
            "dt": "Project",
            "fieldname": "custom_total_project_labor_",
            "label": "Total Project Labor (₹)",
            "fieldtype": "Currency",
            "insert_after": "custom_total_project_material_"
        },
        {
            "dt": "Project",
            "fieldname": "custom_grant_total",
            "label": "Grant Total",
            "fieldtype": "Column Break",
            "insert_after": "custom_total_project_labor_"
        },
        {
            "dt": "Project",
            "fieldname": "custom_total_project_cost_",
            "label": "Total Project Cost (₹)",
            "fieldtype": "Currency",
            "insert_after": "custom_grant_total"
        }
    ]

    for field in fields:
        if not frappe.db.exists(
            "Custom Field",
            {"dt": field["dt"], "fieldname": field["fieldname"]}
        ):
            frappe.get_doc({
                "doctype": "Custom Field",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()
