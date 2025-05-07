"""Initial database schema

Revision ID: 001
Create Date: 2024-01-20
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Create initial database schema."""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create images table
    op.create_table(
        'images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('upload_date', sa.DateTime(), nullable=True),
        sa.Column('metadata', JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create predictions table
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.Integer(), nullable=False),
        sa.Column('prediction_type', sa.String(length=50), nullable=False),
        sa.Column('result_data', JSON, nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create analysis_history table
    op.create_table(
        'analysis_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('image_id', sa.Integer(), nullable=False),
        sa.Column('prediction_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
        sa.ForeignKeyConstraint(['prediction_id'], ['predictions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better query performance
    op.create_index(op.f('ix_images_user_id'), 'images', ['user_id'], unique=False)
    op.create_index(op.f('ix_predictions_image_id'), 'predictions', ['image_id'], unique=False)
    op.create_index(op.f('ix_analysis_history_user_id'), 'analysis_history', ['user_id'], unique=False)
    op.create_index(op.f('ix_analysis_history_image_id'), 'analysis_history', ['image_id'], unique=False)
    op.create_index(op.f('ix_analysis_history_prediction_id'), 'analysis_history', ['prediction_id'], unique=False)

def downgrade() -> None:
    """Remove all tables in reverse order."""
    # Drop indexes first
    op.drop_index(op.f('ix_analysis_history_prediction_id'), table_name='analysis_history')
    op.drop_index(op.f('ix_analysis_history_image_id'), table_name='analysis_history')
    op.drop_index(op.f('ix_analysis_history_user_id'), table_name='analysis_history')
    op.drop_index(op.f('ix_predictions_image_id'), table_name='predictions')
    op.drop_index(op.f('ix_images_user_id'), table_name='images')
    
    # Drop tables
    op.drop_table('analysis_history')
    op.drop_table('predictions')
    op.drop_table('images')
    op.drop_table('users') 