"""change enrol name

Revision ID: 4d08341b5953
Revises: bfd4f2170fcd
Create Date: 2024-04-24 11:10:55.097042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '4d08341b5953'
down_revision: Union[str, None] = 'bfd4f2170fcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mdl_enrol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('enrol', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('courseid', sa.Integer(), nullable=False),
    sa.Column('sortorder', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('enrolperiod', sa.Integer(), nullable=False),
    sa.Column('enrolstartdate', sa.Integer(), nullable=False),
    sa.Column('enrolenddate', sa.Integer(), nullable=False),
    sa.Column('expirynotify', sa.Integer(), nullable=False),
    sa.Column('expirythreshold', sa.Integer(), nullable=False),
    sa.Column('notifyall', sa.Integer(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cost', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('roleid', sa.Integer(), nullable=False),
    sa.Column('customint1', sa.Integer(), nullable=False),
    sa.Column('customint2', sa.Integer(), nullable=False),
    sa.Column('customint3', sa.Integer(), nullable=False),
    sa.Column('customint4', sa.Integer(), nullable=False),
    sa.Column('customint5', sa.Integer(), nullable=False),
    sa.Column('customint6', sa.Integer(), nullable=False),
    sa.Column('customint7', sa.Integer(), nullable=False),
    sa.Column('customint8', sa.Integer(), nullable=False),
    sa.Column('customchar1', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customchar2', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customchar3', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customdec1', sa.Float(), nullable=False),
    sa.Column('customdec2', sa.Float(), nullable=False),
    sa.Column('customtext1', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customtext2', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customtext3', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('customtext4', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('timecreated', sa.Integer(), nullable=False),
    sa.Column('timemodified', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('enrol')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enrol',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('enrol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('courseid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sortorder', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('enrolperiod', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('enrolstartdate', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('enrolenddate', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('expirynotify', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('expirythreshold', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('notifyall', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('cost', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('currency', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('roleid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint2', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint3', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint4', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint5', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint6', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint7', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customint8', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('customchar1', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customchar2', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customchar3', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customdec1', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('customdec2', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('customtext1', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customtext2', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customtext3', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('customtext4', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timecreated', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('timemodified', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='enrol_pkey')
    )
    op.drop_table('mdl_enrol')
    # ### end Alembic commands ###
