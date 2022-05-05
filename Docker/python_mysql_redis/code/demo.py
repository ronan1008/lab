from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
BASE = declarative_base()


class User(BASE):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String(64), unique=True)
    password = sa.Column(sa.String(64))
    email = sa.Column(sa.String(128),unique=True)
    create_at = sa.Column(sa.DateTime, server_default= sa.func.now())

    def __repr__(self):
        return "id={}, username={}, email={}".format(
            self.id, self.username, self.email
        )


engine = sa.create_engine("mysql+pymysql://root:mysql@mysql:3306/demo" , echo= True)
engine = sa.create_engine("mysql+pymysql://root:mysql@mysql:3306/demo")

Session = sa.orm.sessionmaker(bind=engine)
BASE.metadata.create_all(engine)

# user2 = User(username='test2', password='test1', email='ronan1002@yahoo.com.tw')
# user3 = User(username='test3', password='test1', email='ronan1003@yahoo.com.tw')

# session = Session()
# session.add_all([user2, user3])
# session.commit()

# s = Session()

# users = s.query(User)
# print(users)

# for u in users:
#     print(u)

# s = Session()
# users = s.query(User).filter(User.username == 'test1')
# print(users)
# for u in users:
#     print(u)

# s = Session()
# users = s.query(User).order_by(User.id.desc())
# for u in users:
#     print(u)

# s = Session()
# users = s.query(User).all()
# print(users)

# s = Session()
# users = s.query(User).filter(User.username == 'test1').first()

# if users:
#     print('user name exit')
#     pass
# else:
#     pass

# s = Session()
# users = s.query(User).order_by(User.id.desc()).limit(2).all()
# print(users)
# for u in users:
#     print(u)

# s = Session()
# users = s.query(User).filter(User.username.in_(['test2','test3']))
# for u in users:
#     print(u)

# s = Session()
# users = s.query(User).filter(User.username.like("%es%"))
# for u in users:
#     print(u)


# s = Session()
# u1 = s.query(User)
# for u in u1:
#     print(u, type(u))

# u2 = s.query(User.id, User.username)
# for u in u2:
#     print(u, type(u))

# s = Session()
# users = s.query(User).filter(User.username.like("%st1%"))
# for u in users:
#     print(u)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM user"))
    # for r in result:
    #     print(r.username)
    for dict_row in result.mappings():
        x = dict_row['username']
        y = dict_row['id']
        z = dict_row['password']
        # print(x)
        print(y)
        print(z)
