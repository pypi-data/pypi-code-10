"""
WebPortfolio

model.py

You may place your models here.
"""

from active_alchemy import SQLAlchemy
import config
from webportfolio import init_app, get_env_config
from webportfolio.packages import user, cms

# The config
conf = get_env_config(config)

# Connect the DB
db = SQLAlchemy(conf.SQL_URI)

# Attach the Active SQLAlchemy
init_app(db.init_app)

# ------------------------------------------------------------------------------

# User Model
User = user.model(db)

# Post Model
Cms = cms.model(User)

# A simple my_note table example
class MyNote(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.User.id))
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    user = db.relationship(User.User, backref="notes")
