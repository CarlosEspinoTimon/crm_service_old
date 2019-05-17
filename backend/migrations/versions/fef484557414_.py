"""empty message

Revision ID: fef484557414
Revises: 
Create Date: 2019-05-17 17:01:50.060963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fef484557414'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.Column('admin_privileges_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modify_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('modify_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_privileges_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['modify_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_admin'), 'user', ['admin'], unique=False)
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_modify_at'), 'user', ['modify_at'], unique=False)
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('surname', sa.String(length=120), nullable=True),
    sa.Column('photo_url', sa.String(length=120), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modify_by', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('last_modify_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_at'], ['user.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_last_modify_at'), 'customer', ['last_modify_at'], unique=False)
    op.create_index(op.f('ix_customer_last_modify_by'), 'customer', ['last_modify_by'], unique=False)
    op.create_index(op.f('ix_customer_name'), 'customer', ['name'], unique=False)
    op.create_index(op.f('ix_customer_photo_url'), 'customer', ['photo_url'], unique=False)
    op.create_index(op.f('ix_customer_surname'), 'customer', ['surname'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customer_surname'), table_name='customer')
    op.drop_index(op.f('ix_customer_photo_url'), table_name='customer')
    op.drop_index(op.f('ix_customer_name'), table_name='customer')
    op.drop_index(op.f('ix_customer_last_modify_by'), table_name='customer')
    op.drop_index(op.f('ix_customer_last_modify_at'), table_name='customer')
    op.drop_table('customer')
    op.drop_index(op.f('ix_user_modify_at'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_index(op.f('ix_user_admin'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
