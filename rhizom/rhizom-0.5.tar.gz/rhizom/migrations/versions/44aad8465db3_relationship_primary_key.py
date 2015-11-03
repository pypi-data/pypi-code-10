"""Relationship primary key

Revision ID: 44aad8465db3
Revises: b331d042fca
Create Date: 2015-10-14 11:05:12.129315

"""

# revision identifiers, used by Alembic.
revision = '44aad8465db3'
down_revision = 'b331d042fca'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from rhizom.database import is_sqlite, exists_in_db


old_table = sa.sql.table('relationships_old',
    sa.sql.column('source_id', sa.Integer),
    sa.sql.column('target_id', sa.Integer),
    sa.sql.column('type_name', sa.Unicode),
    sa.sql.column('graph_id', sa.Integer),
    sa.sql.column('dotted', sa.Boolean),
    )

def upgrade():
    connection = op.get_bind()
    op.drop_constraint(
        op.f('fk_relationships_graph_id_relationship_types'),
        "relationships", type_="foreignkey")
    op.drop_constraint(
        op.f('fk_relationships_graph_id_graphs'),
        "relationships", type_="foreignkey")
    op.drop_constraint(
        op.f('fk_relationships_source_id_persons'),
        "relationships", type_="foreignkey")
    op.drop_constraint(
        op.f('fk_relationships_target_id_persons'),
        "relationships", type_="foreignkey")
    op.rename_table('relationships', 'relationships_old')
    new_table = op.create_table('relationships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('type_name', sa.Unicode(length=32), nullable=False),
        sa.Column('graph_id', sa.Integer(), nullable=False),
        sa.Column('dotted', sa.Boolean(), server_default=sa.text('0'), nullable=False),
        sa.ForeignKeyConstraint(['graph_id', 'type_name'],
            ['relationship_types.graph_id', 'relationship_types.name'],
            name=op.f('fk_relationships_graph_id_relationship_types'),
            onupdate=u'cascade', ondelete=u'cascade'),
        sa.ForeignKeyConstraint(['graph_id'], [u'graphs.id'],
            name=op.f('fk_relationships_graph_id_graphs')),
        sa.ForeignKeyConstraint(['source_id'], [u'persons.id'],
            name=op.f('fk_relationships_source_id_persons'),
            onupdate=u'cascade', ondelete=u'cascade'),
        sa.ForeignKeyConstraint(['target_id'], [u'persons.id'],
            name=op.f('fk_relationships_target_id_persons'),
            onupdate=u'cascade', ondelete=u'cascade'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_relationships'))
    )
    for rel in connection.execute(old_table.select()).fetchall():
        connection.execute(new_table.insert().values(
            source_id=rel["source_id"],
            target_id=rel["target_id"],
            type_name=rel["type_name"],
            graph_id=rel["graph_id"],
            dotted=rel["dotted"],
            ))
    op.drop_table('relationships_old')


def downgrade():
    raise RuntimeError
