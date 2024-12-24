# apps/erpnext/erpnext/customapi.py
import frappe
@frappe.whitelist()
def get_workflow_actions(doctype, workflow_state, owner=None):
    # Ensure proper validation
    if not (doctype and workflow_state):
        frappe.throw("Doctype and workflow_state are required parameters.")

    # Validate if the owner is a customer
    if owner:
        owner_type = frappe.db.get_value('User', owner, 'user_type')
        if owner_type != 'Customer':
            return []

    # Fetch all Workflow Transitions
    all_workflow_transitions = frappe.get_all(
        'Workflow Transition',
        fields=['state', 'action', 'next_state']
    )

    # Apply filtering logic manually
    filtered_workflow = [
        transition
        for transition in all_workflow_transitions
        if transition['state'] == workflow_state
    ]

    # Return the filtered results
    return filtered_workflow


import frappe
from frappe.workflow.doctype.workflow_action.workflow_action import WorkflowAction

@frappe.whitelist()
def update_workflow_state(docname, action):
    # Get the document
    doc = frappe.get_doc('Issue', docname)

    # Ensure the action exists in the available actions for the current state
    if action in doc.workflow_state_actions:
        # Trigger the workflow action
        WorkflowAction.trigger(doc, action)
        frappe.db.commit()  # Commit the changes to the database
        return {"status": "success", "message": f"Workflow state updated to {doc.workflow_state}"}
    else:
        return {"status": "error", "message": f"Invalid action '{action}' for current state '{doc.workflow_state}'"}
