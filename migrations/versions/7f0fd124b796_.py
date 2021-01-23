"""empty message

Revision ID: 7f0fd124b796
Revises: 
Create Date: 2021-01-02 16:13:38.003716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f0fd124b796'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('type', sa.Enum('image', 'youtube', 'video_url', 'spotify', 'apple_music', name='mediatype'), nullable=False),
    sa.Column('caption', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('creative',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.Column('profile_image_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.Column('instagram_username', sa.String(), nullable=True),
    sa.Column('twitter_username', sa.String(), nullable=True),
    sa.Column('facebook_username', sa.String(), nullable=True),
    sa.Column('bandcamp_username', sa.String(), nullable=True),
    sa.Column('reddit_username', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profile_image_id'], ['media.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['creative.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('project_creatives',
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('creative_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creative_id'], ['creative.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project_creatives')
    op.drop_table('project')
    op.drop_table('creative')
    op.drop_table('media')
    # ### end Alembic commands ###
