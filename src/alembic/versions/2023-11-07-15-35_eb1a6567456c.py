"""empty message

Revision ID: eb1a6567456c
Revises:
Create Date: 2023-11-07 15:35:08.955263

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "eb1a6567456c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Add the is_active column default to True
    op.add_column("repository", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.false()))
    # Updates using value of removed_at
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    try:
        # Update is_active to True where removed_at is NULL
        session.execute("UPDATE repository SET is_active = (removed_at IS NULL)")
        session.commit()
    finally:
        session.close()
    # Remove the legacy column
    op.drop_column("repository", "removed_at")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("repository", sa.Column("removed_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    # Use a session to update the removed_at column based on is_active being False
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    try:
        # Set removed_at to a specific time where is_active is False
        # You may choose to leave it as NULL or set it to a specific timestamp
        session.execute(
            "UPDATE repository SET removed_at = CASE WHEN is_active = false THEN CURRENT_TIMESTAMP ELSE NULL END"
        )
        session.commit()
    finally:
        session.close()
    # Remove the column
    op.drop_column("repository", "is_active")
    # ### end Alembic commands ###
