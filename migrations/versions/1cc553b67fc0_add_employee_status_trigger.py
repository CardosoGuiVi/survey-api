"""add employee status trigger

Revision ID: 1cc553b67fc0
Revises: 4ef05a8f5479
Create Date: 2026-04-16 12:37:01.867976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cc553b67fc0'
down_revision: Union[str, Sequence[str], None] = '4ef05a8f5479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION update_employee_status()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.type IN ('hired', 'rehired') THEN
                UPDATE employees SET status = 'active'
                WHERE id = NEW.employee_id;
            ELSIF NEW.type IN ('resigned', 'terminated', 'deceased') THEN
                UPDATE employees SET status = 'inactive'
                WHERE id = NEW.employee_id;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_update_employee_status
        AFTER INSERT ON employee_events
        FOR EACH ROW EXECUTE FUNCTION update_employee_status();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_update_employee_status ON employee_events")
    op.execute("DROP FUNCTION IF EXISTS update_employee_status")
