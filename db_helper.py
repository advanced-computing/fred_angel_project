# This file will contain the code to make a user table

import duckdb



def create_db(name: str):
    try:
       con = duckdb.connect(name)
       print(f'{name} created')
       
       con.close()
    except Exception as e:
        print('error: ', e)
 
# only need to do this once I suppose        
#create_db('un_data.db')





