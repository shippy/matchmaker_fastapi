"""Add

Revision ID: 795dfcc77bc5
Revises: 9c6dd0e0f5b7
Create Date: 2023-05-17 21:28:19.422900

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '795dfcc77bc5'
down_revision = '9c6dd0e0f5b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('message', sa.JSON(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    # ### end Alembic commands ###