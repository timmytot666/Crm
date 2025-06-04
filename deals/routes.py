from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from deals.models import Deal, PipelineStage
from deals.forms import DealForm
from urllib.parse import quote_plus
from common.utils import generate_entity_email_body, generate_pipeline_summary_email_body # Added new import
from sqlalchemy import func
from decimal import Decimal # Ensure Decimal is available for stage_totals sums

deals_bp = Blueprint('deals', __name__, template_folder='../templates/deals')

@deals_bp.route('/')
@login_required
def list_deals():
    deals = Deal.query.filter_by(user_id=current_user.id).order_by(Deal.expected_close_date.desc()).all()
    return render_template('list_deals.html', deals=deals, title='All Deals')

@deals_bp.route('/pipeline')
@login_required
def pipeline_view():
    stages = PipelineStage.query.order_by(PipelineStage.order).all()
    deals_by_stage = {}
    stage_totals = {}
    for stage in stages:
        deals_in_stage = Deal.query.filter_by(user_id=current_user.id, pipeline_stage_id=stage.id).all()
        deals_by_stage[stage.id] = deals_in_stage
        # Ensure values are Decimal for sum, or handle None
        stage_totals[stage.id] = sum(deal.value for deal in deals_in_stage if deal.value is not None) or Decimal(0)

    pipeline_email_subject = "CRM - Deal Pipeline Summary"
    pipeline_email_body = generate_pipeline_summary_email_body(stages, deals_by_stage, stage_totals)
    pipeline_mailto_link = f"mailto:?subject={quote_plus(pipeline_email_subject)}&body={quote_plus(pipeline_email_body)}".replace('+', '%20')

    return render_template('pipeline_view.html', stages=stages, deals_by_stage=deals_by_stage, stage_totals=stage_totals, title='Deal Pipeline', pipeline_mailto_link=pipeline_mailto_link)

@deals_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_deal():
    form = DealForm()
    if form.validate_on_submit():
        deal = Deal(
            name=form.name.data,
            value=form.value.data,
            expected_close_date=form.expected_close_date.data,
            probability=form.probability.data,
            pipeline_stage_id=form.pipeline_stage_id.data,
            contact_id=form.contact_id.data if form.contact_id.data != 0 else None,
            company_id=form.company_id.data if form.company_id.data != 0 else None,
            user_id=current_user.id
        )
        db.session.add(deal)
        db.session.commit()
        flash('Deal created successfully!', 'success')
        return redirect(url_for('deals.pipeline_view'))
    return render_template('create_edit_deal.html', form=form, title='Create Deal')

@deals_bp.route('/<int:deal_id>/view')
@login_required
def view_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)

    email_subject = f"CRM Deal Information: {deal.name}"
    email_body = generate_entity_email_body(deal)
    mailto_link = f"mailto:?subject={quote_plus(email_subject)}&body={quote_plus(email_body)}".replace('+', '%20')

    return render_template('view_deal.html', deal=deal, title=deal.name, mailto_link=mailto_link)

@deals_bp.route('/<int:deal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    form = DealForm(obj=deal)
    if form.validate_on_submit():
        deal.name = form.name.data
        deal.value = form.value.data
        deal.expected_close_date = form.expected_close_date.data
        deal.probability = form.probability.data
        deal.pipeline_stage_id = form.pipeline_stage_id.data
        deal.contact_id = form.contact_id.data if form.contact_id.data != 0 else None
        deal.company_id = form.company_id.data if form.company_id.data != 0 else None
        db.session.commit()
        flash('Deal updated successfully!', 'success')
        return redirect(url_for('deals.view_deal', deal_id=deal.id))
    return render_template('create_edit_deal.html', form=form, title='Edit Deal', deal=deal)

@deals_bp.route('/<int:deal_id>/delete', methods=['POST'])
@login_required
def delete_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()
    flash('Deal deleted successfully!', 'success')
    return redirect(url_for('deals.pipeline_view'))
