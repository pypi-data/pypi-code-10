'''WasPosted mapping for SQLAlchemy'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

MYBASE = declarative_base()

class WasPosted(MYBASE):
    '''WasPosted mapping for SQLAlchemy'''
    __tablename__ = 'wasposted'
    tweet = Column(String, primary_key=True)
    lastinsertid = Column(Integer)
