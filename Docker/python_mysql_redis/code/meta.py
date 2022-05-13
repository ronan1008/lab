from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey

engine = create_engine("mysql+pymysql://root:mysql@mysql:3306/demo" , echo= True)

# metadata_obj = MetaData()
# user_table = Table(
#     "user_account",
#     metadata_obj,
#     Column('id', Integer(), primary_key=True),
#     Column('name', String(30)),
#     Column('fullname', String(30))
# )


# address_table = Table(
#     "address",
#     metadata_obj,
#     Column('id', Integer(), primary_key=True),
#     Column('user_id', ForeignKey('user_account.id'), nullable=False),
#     Column('email_address', String(30), nullable=False)
# )
# metadata_obj.create_all(engine)


#orm

from sqlalchemy.orm import declarative_base
Base = declarative_base()

from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(30))
    addresses = relationship("Address", back_populates="user")
    def __repr__(self):
       return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

Base.metadata.create_all(engine)


from sqlalchemy import insert
stmt = insert(User).values(name='spongebob', fullname="Spongebob Squarepants")
print(stmt)
compiled = stmt.compile()
print(compiled)

print(compiled.params)