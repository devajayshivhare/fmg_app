import frappe
from frappe.utils import escape_html, fmt_money

@frappe.whitelist()
def send_project_proposal(project_name):
    # ✅ Fetch main doc + users child table
    project = frappe.get_doc("Project", project_name)
    
    # 🔍 Get client email from 'users' child table
    recipient = None
    
    # Loop through 'users' table (field name may be 'users' or 'project_users' — adjust if needed)
    for user_row in (project.users or []):  # ← field name must match your child table fieldname
        # Try common field names
        email = None
        
        # Option 1: Direct email field
        if hasattr(user_row, 'email_id'):
            email = user_row.email_id
        elif hasattr(user_row, 'email'):
            email = user_row.email
        
        # Option 2: Link to User (get email from User doc)
        elif hasattr(user_row, 'user') and user_row.user:
            email = frappe.db.get_value("User", user_row.user, "email")
        
        # Only use if role is 'Client' (optional but recommended)
        role = getattr(user_row, 'role', '').lower()
        if email and (not role or 'client' in role):
            recipient = email
            break
    
    if not recipient:
        # Fallback: try top-level fields
        for field in ["client_email", "email_id", "contact_email"]:
            if hasattr(project, field):
                recipient = getattr(project, field)
                if recipient:
                    break
    
    if not recipient:
        frappe.throw("❌ No client email found. Please add a client in the 'Users' table with an email.")
    
    # Build HTML (same as before)
    table_rows = ""
    grand_total = 0
    for item in project.custom_resource_plan or []:
        desc = escape_html(item.description or item.item_code or "—")
        total = item.total_rs or 0
        grand_total += total
        table_rows += f"""
            <tr>
                <td style="padding:8px;border:1px solid #ddd;">{desc}</td>
                <td style="padding:8px;border:1px solid #ddd;text-align:right;">
                    {fmt_money(total, currency="INR")}
                </td>
            </tr>
        """
    
    html = f"""
        <div style="font-family:Arial,sans-serif;max-width:800px;margin:0 auto;">
            <h2>Project Proposal: {escape_html(project.project_name or project.name)}</h2>
            <p><strong>Client:</strong> {escape_html(project.customer or project.users[0].full_name or '—')}</p>
            <p><strong>Date:</strong> {frappe.utils.nowdate()}</p>
            <h3>Scope of Work</h3>
            <table style="width:100%;border-collapse:collapse;margin:12px 0;">
                <thead><tr style="background:#f8f9fa;">
                    <th style="padding:10px;border:1px solid #ddd;text-align:left;">Description</th>
                    <th style="padding:10px;border:1px solid #ddd;text-align:right;">Amount</th>
                </tr></thead>
                <tbody>{table_rows}</tbody>
                <tfoot><tr style="background:#e9ecef;font-weight:bold;">
                    <td style="padding:10px;border:1px solid #ddd;">Grand Total</td>
                    <td style="padding:10px;border:1px solid #ddd;text-align:right;">
                        {fmt_money(grand_total, currency="INR")}
                    </td>
                </tr></tfoot>
            </table>
            <p><em>Thank you for your consideration.</em></p>
        </div>
    """
    
    # ✅ Send email
    frappe.sendmail(
        recipients=[recipient],
        subject=f"Proposal: {project.project_name or project.name}",
        message=html,
        reference_doctype="Project",
        reference_name=project.name,
        now=True
    )
    
    return {"message": f"✅ Proposal sent to {recipient}!"}