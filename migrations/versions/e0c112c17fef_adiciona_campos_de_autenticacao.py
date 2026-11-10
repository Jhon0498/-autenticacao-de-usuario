
"""adiciona campos de autenticacao
Revision ID: e0c112c17fef
Revises: 4a43fa1978b0
Create Date: 2026-11-10 00:20:47.075088
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e0c112c17fef'
down_revision = '4a43fa1978b0'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona os campos necessários para autenticação.
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('email', sa.String(length=64), nullable=True)
        )
        batch_op.add_column(
            sa.Column('password_hash', sa.String(length=128), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                'confirmed',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )
        batch_op.create_index(
            batch_op.f('ix_users_email'),
            ['email'],
            unique=True
        )


def downgrade():
    # Remove somente os campos adicionados nesta migração.
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_column('confirmed')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')
