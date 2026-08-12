from alembic import op
import sqlalchemy as sa

revision = '0b1a6d0c2e35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'health_checks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('service_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('health_checks')
