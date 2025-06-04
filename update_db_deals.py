from app import app, db
from deals.models import Deal, PipelineStage

with app.app_context():
    print('Creating deal and pipeline_stage tables...')
    db.create_all()
    print('Inserting initial pipeline stages...')
    PipelineStage.insert_initial_stages()
    print('Deal and pipeline stage tables check/creation and initialization complete.')
