from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class FirefoxBookmarks(Base):
    __tablename__ = 'moz_bookmarks'
    id = Column(Integer, primary_key=True)
    title = Column(Text, index=True)
    parent = Column(Integer, ForeignKey('moz_bookmarks.id'), nullable=True)
    children = relationship('FirefoxBookmarks',
                            # cascade deletions
                            cascade='all',
                            # remote_side is required to reference
                            # the 'remote' column in the join condition
                            backref=backref('parent_object',
                                            remote_side='FirefoxBookmarks.id'))

    def __repr__(self):
        return self.title or ''
