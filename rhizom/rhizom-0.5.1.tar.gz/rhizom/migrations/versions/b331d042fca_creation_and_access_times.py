"""Creation and access times

Revision ID: b331d042fca
Revises: 3a74acdf7764
Create Date: 2015-10-07 20:49:10.397408

"""

# revision identifiers, used by Alembic.
revision = 'b331d042fca'
down_revision = '3a74acdf7764'
branch_labels = None
depends_on = None

from datetime import datetime

import sqlalchemy as sa
from alembic import op
from rhizom.database import is_sqlite, exists_in_db


def upgrade():
    conn = op.get_bind()
    op.add_column('graphs', sa.Column('creation', sa.DateTime(), nullable=True))
    op.add_column('graphs', sa.Column('last_access', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('creation', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_connection', sa.DateTime(), nullable=True))
    graph_table = sa.sql.table('graphs',
        sa.sql.column('creation', sa.DateTime),
        sa.sql.column('last_access', sa.DateTime),
        )
    users_table = sa.sql.table('users',
        sa.sql.column('creation', sa.DateTime),
        sa.sql.column('last_connection', sa.DateTime),
        )
    conn.execute(graph_table.update().values(
        creation=datetime.utcnow(), last_access=datetime.utcnow()))
    conn.execute(users_table.update().values(
        creation=datetime.utcnow(), last_connection=datetime.utcnow()))
    if is_sqlite(conn):
        op.alter_column('graphs', 'creation', nullable=False)
        op.alter_column('graphs', 'last_access', nullable=False)
        op.alter_column('users', 'creation', nullable=False)
        op.alter_column('users', 'last_connection', nullable=False)



def downgrade():
    if not is_sqlite(op.get_bind()):
        op.drop_column('users', 'last_connection')
        op.drop_column('users', 'creation')
        op.drop_column('graphs', 'last_access')
        op.drop_column('graphs', 'creation')
