"""add all tables

Revision ID: d9e128afb309
Revises: 
Create Date: 2020-05-27 12:33:38.257309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9e128afb309'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('cases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('casename', sa.String(), nullable=True),
    sa.Column('creator', sa.String(), nullable=True),
    sa.Column('createdate', sa.String(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('flashpoint', sa.Integer(), nullable=True),
    sa.Column('crowdstrike', sa.Integer(), nullable=True),
    sa.Column('postgres', sa.Integer(), nullable=True),
    sa.Column('virustotal', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('btcaddresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('indicator', sa.String(length=255), nullable=True),
    sa.Column('event', sa.Text(), nullable=True),
    sa.Column('platform', sa.String(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('filename',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ipaddresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=24), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('keywords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('md5',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('names',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('author', sa.String(length=32), nullable=True),
    sa.Column('createdate', sa.String(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.Integer(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sha1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sha256',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('slackwebhook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slackwebhook', sa.String(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(length=120), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('userids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.Integer(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usernames',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('indicator', sa.String(), nullable=True),
    sa.Column('caseid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usernames')
    op.drop_table('userids')
    op.drop_table('urls')
    op.drop_table('slackwebhook')
    op.drop_table('sha256')
    op.drop_table('sha1')
    op.drop_table('phones')
    op.drop_table('notes')
    op.drop_table('names')
    op.drop_table('md5')
    op.drop_table('keywords')
    op.drop_table('ipaddresses')
    op.drop_table('filename')
    op.drop_table('events')
    op.drop_table('emails')
    op.drop_table('domains')
    op.drop_table('btcaddresses')
    op.drop_table('cases')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
