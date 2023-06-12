"""pass

Revision ID: b9bc62717ab8
Revises: 8a3528d4f806
Create Date: 2022-12-07 14:56:15.768155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9bc62717ab8'
down_revision = '8a3528d4f806'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.drop_column('password1')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password1', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###