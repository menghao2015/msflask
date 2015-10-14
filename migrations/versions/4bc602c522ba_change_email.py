"""change_email

Revision ID: 4bc602c522ba
Revises: 12582d318057
Create Date: 2015-10-13 23:52:42.628613

"""

# revision identifiers, used by Alembic.
revision = '4bc602c522ba'
down_revision = '12582d318057'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('temp_email', sa.String(length=64), nullable=True))
    op.create_unique_constraint(None, 'users', ['temp_email'])
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'temp_email')
    ### end Alembic commands ###
