from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Code(Base):
    __tablename__ = 'Code'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(250), nullable=False)
    language = Column(String(50), nullable=False)
    code = Column(Text, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self):
        return "<Code(%d, '%s', '%s','%s', %d)>" % (self.id, self.description, self.language, self.code, self.user_id)
