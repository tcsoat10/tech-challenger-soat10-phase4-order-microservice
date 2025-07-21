"""populate order status table

Revision ID: f2b67da5636f47
Revises: f2b67da5636f46
Create Date: 2025-07-20 22:06:13.227579

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

from src.constants.order_status import OrderStatusEnum


# revision identifiers, used by Alembic.
revision: str = 'f2b67da5636f47'
down_revision: Union[str, None] = 'b67da5636f46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


order_status_table = table(
    'order_status',
    column('id', Integer),
    column('status', String),
    column('description', String)
)

order_statuses = [*OrderStatusEnum.values_and_descriptions()]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(order_status_table, order_statuses)


def downgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.execute(
        f"DELETE FROM order_status WHERE status IN ({', '.join([f'\'{order_status.status}\'' for order_status in OrderStatusEnum])})"
    )