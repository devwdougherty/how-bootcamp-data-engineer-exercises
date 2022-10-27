from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')

sql = '''
select * from view_web_site
'''

df = pd.read_sql_query(sql, engine)

sql_insert = '''
INSERT INTO public.tb_web_site
("date", "rank", artist)
VALUES('2022-12-20', 10, 'Will');
'''

engine.execute(sql_insert)