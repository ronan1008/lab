from sqlalchemy import create_engine, text
from pprint import pprint



engine = create_engine("mysql+pymysql://root:mysql@mysql:3306/demo" , echo= True)
with engine.connect() as conn:
    result = conn.execute(text("Select * From users"))


pprint(result.all())


with engine.begin() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(text(
        "INSERT INTO some_table (x,y) VALUES(:x,:y)"),
        [{"x":1, "y":1}, {"x":2, "y": 4}]
    )
