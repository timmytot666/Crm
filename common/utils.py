from flask import current_app
from decimal import Decimal # Moved to top

# Import models to check instance types
from contacts.models import Contact
from companies.models import Company
from deals.models import Deal, PipelineStage

def format_currency(value):
    if isinstance(value, Decimal) or isinstance(value, float):
        return f"${value:,.2f}"
    if isinstance(value, int): # Handle integers too
        return f"${Decimal(value):,.2f}"
    return str(value) if value is not None else 'N/A' # Handle None

def generate_entity_email_body(entity):
    body_lines = []
    # crm_base_url = current_app.config.get('APP_BASE_URL', 'YOUR_CRM_URL') # For generating links if needed

    if isinstance(entity, Deal):
        body_lines.append(f"Deal Information:")
        body_lines.append(f"--------------------------")
        body_lines.append(f"Name: {entity.name}")
        if entity.stage:
            body_lines.append(f"Stage: {entity.stage.name}")
        body_lines.append(f"Value: {format_currency(entity.value)}")
        body_lines.append(f"Expected Close Date: {entity.expected_close_date.strftime('%Y-%m-%d') if entity.expected_close_date else 'N/A'}")
        if entity.company:
            body_lines.append(f"Associated Company: {entity.company.name}")
        if entity.contact:
            body_lines.append(f"Associated Contact: {entity.contact.name}")
        # body_lines.append(f"Link: {crm_base_url}/deals/{entity.id}/view")

    elif isinstance(entity, Contact):
        body_lines.append(f"Contact Information:")
        body_lines.append(f"--------------------------")
        body_lines.append(f"Name: {entity.name}")
        body_lines.append(f"Email: {entity.email if entity.email else 'N/A'}")
        body_lines.append(f"Primary Phone: {entity.phone_primary if entity.phone_primary else 'N/A'}")
        if entity.company:
            body_lines.append(f"Company: {entity.company.name}")
        if entity.tags:
            body_lines.append(f"Tags: {entity.tags}")
        # body_lines.append(f"Link: {crm_base_url}/contacts/{entity.id}/view")

    elif isinstance(entity, Company):
        body_lines.append(f"Company Information:")
        body_lines.append(f"--------------------------")
        body_lines.append(f"Name: {entity.name}")
        body_lines.append(f"Industry: {entity.industry if entity.industry else 'N/A'}")
        body_lines.append(f"Website: {entity.website if entity.website else 'N/A'}")
        body_lines.append(f"Primary Contact Name: {entity.primary_contact_name if entity.primary_contact_name else 'N/A'}")
        if entity.address: # Keep address concise
            address_summary = (entity.address[:75] + '...') if len(entity.address) > 75 else entity.address
            body_lines.append(f"Address: {address_summary.replace('\n', ', ')}")
        # body_lines.append(f"Link: {crm_base_url}/companies/{entity.id}/view")
    else:
        return "No information available for this entity type."

    return '\n'.join(body_lines)

def generate_pipeline_summary_email_body(stages, deals_by_stage, stage_totals):
    body_lines = ["Deal Pipeline Summary:"]
    body_lines.append("--------------------------")
    overall_total_value = Decimal(0)

    for stage in stages:
        num_deals = len(deals_by_stage.get(stage.id, []))
        total_value = Decimal(stage_totals.get(stage.id, 0)) # Ensure Decimal for consistent formatting
        overall_total_value += total_value
        body_lines.append(f"\nStage: {stage.name}") # Added newline for better spacing
        body_lines.append(f"  Deals: {num_deals}")
        body_lines.append(f"  Total Value: {format_currency(total_value)}")
    body_lines.append("--------------------------")
    body_lines.append(f"\nOverall Pipeline Value: {format_currency(overall_total_value)}")
    return '\n'.join(body_lines)
