import frappe

# def run():
#     print("Running setup script...")
#     # your logic here

def setup_project():
    print("\n--- STARTING PROJECT SETUP SCRIPT ---\n")

    # -------------------------------------------------
    # 1️⃣ CHILD DOCTYPES DEFINITIONS
    # -------------------------------------------------

    child_doctypes = [
        {
            "name": "Project Resource Plan",
            "fields": [
                {"fieldname": "resource", "label": "Resource", "fieldtype": "Link", "options": "Employee", "in_list_view": 1},
                {"fieldname": "hours", "label": "Hours", "fieldtype": "Float", "in_list_view": 1},
                {"fieldname": "cost", "label": "Cost", "fieldtype": "Currency", "in_list_view": 1},
            ]
        },
        {
            "name": "Material Coverage Details",
            "fields": [
                {"fieldname": "material", "label": "Material", "fieldtype": "Link", "options": "Item", "in_list_view": 1},
                {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Float", "in_list_view": 1},
                {"fieldname": "coverage_area", "label": "Coverage Area", "fieldtype": "Float", "in_list_view": 1},
            ]
        }
    ]

    for d in child_doctypes:
        if frappe.db.exists("DocType", d["name"]):
            print(f"✔ Child Doctype already exists: {d['name']}")
            continue

        frappe.get_doc({
            "doctype": "DocType",
            "name": d["name"],
            "module": "FMG",
            "istable": 1,
            "editable_grid": 1,
            "fields": d["fields"]
        }).insert(ignore_permissions=True)

        print(f"✅ Created Child Doctype: {d['name']}")

    # -------------------------------------------------
    # 2️⃣ PROJECT CUSTOM FIELDS + TABLE FIELDS
    # -------------------------------------------------

    project_fields = [
        {"fieldname":"custom_project_planning","label":"Project Planning","fieldtype":"Section Break","insert_after":None},
        {"fieldname":"custom_company_copy","label":"Company Name","fieldtype":"Link","options":"Company","insert_after":"custom_project_planning"},
        {"fieldname":"custom_column_break_osfbk","label":"","fieldtype":"Column Break","insert_after":"custom_company_copy"},
        {"fieldname":"custom_type_of_flooring","label":"Flooring Type","fieldtype":"Link","options":"Item","insert_after":"custom_column_break_osfbk"},
        {"fieldname":"custom_section_break_nf0xo","label":"","fieldtype":"Section Break","insert_after":"custom_type_of_flooring"},
        {"fieldname":"custom_warehouse_area","label":"Flooring Area","fieldtype":"Float","insert_after":"custom_section_break_nf0xo"},
        {"fieldname":"custom_floor_thickness","label":"Floor Thickness","fieldtype":"Float","insert_after":"custom_warehouse_area"},
        {"fieldname":"custom_column_break_es2na","label":"","fieldtype":"Column Break","insert_after":"custom_floor_thickness"},
        {"fieldname":"custom_new_uom","label":"UOM","fieldtype":"Select","options":"Square Meter","insert_after":"custom_column_break_es2na"},
        {"fieldname":"custom_new_uom_thickness","label":"UOM (Thickness)","fieldtype":"Select","options":"Meter","insert_after":"custom_new_uom"},
        {"fieldname":"custom_uom","label":"UOM","fieldtype":"Link","options":"UOM","insert_after":"custom_new_uom_thickness"},
        {"fieldname":"custom_uom_thickness","label":"UOM (Thickness)","fieldtype":"Link","options":"UOM","insert_after":"custom_uom"},
        {"fieldname":"custom_section_break_iw3fy","label":"Project Resource Plan","fieldtype":"Section Break","insert_after":"custom_uom_thickness"},

        # CHILD TABLE FIELDS
        {"fieldname":"custom_resource_plan","label":"Resource Plan","fieldtype":"Table","options":"Project Resource Plan","insert_after":"custom_section_break_iw3fy"},
        {"fieldname":"custom_material_coverage_details","label":"Material Coverage Details","fieldtype":"Table","options":"Material Coverage Details","insert_after":"custom_resource_plan"},

        # COST SUMMARY
        {"fieldname":"custom_project_cost_summary","label":"Project Cost Summary","fieldtype":"Section Break","insert_after":"custom_material_coverage_details"},
        {"fieldname":"custom_total_project_material_","label":"Total Project Material (₹)","fieldtype":"Currency","insert_after":"custom_project_cost_summary"},
        {"fieldname":"custom_total_project_labor_","label":"Total Project Labor (₹)","fieldtype":"Currency","insert_after":"custom_total_project_material_"},
        {"fieldname":"custom_grant_total","label":"Grant Total","fieldtype":"Column Break","insert_after":"custom_total_project_labor_"},
        {"fieldname":"custom_total_project_cost_","label":"Total Project Cost (₹)","fieldtype":"Currency","insert_after":"custom_grant_total"},
    ]

    for f in project_fields:
        if frappe.db.exists("Custom Field", {"dt": "Project", "fieldname": f["fieldname"]}):
            print(f"✔ Project field already exists: {f['fieldname']}")
            continue

        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Project",
            **f
        }).insert(ignore_permissions=True)

        print(f"✅ Created Project field: {f['fieldname']}")

    frappe.db.commit()

    print("\n🎉 PROJECT SETUP COMPLETED SUCCESSFULLY 🎉\n")
