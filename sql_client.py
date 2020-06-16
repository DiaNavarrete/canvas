import sqlalchemy as db
from flask import jsonify


class SQLclient():
    def __init__(self):
        self.connection = None

    # Establecemos la conexion
    def get_connect(self,db_connector, db_user, db_password, db_host, db_port, database): 
            self.connection = db.create_engine(
                '{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db_connector, db_user,
                    db_password, db_host,db_port, database),
            pool_recycle=3600, convert_unicode=True)


    # Metodo para ejecucion de un query select
    def execute_query(self, query):      
        try: 
            data = self.connection.execute(query) 
            try:
                result = [dict(zip(tuple(data.keys()), i)) for i in data.cursor]
            except Exception as e:
                print('ERROR',e)
                result = data.cursor._rows
        except Exception as e:
            raise
        
        return result


    # Metodo para ejecucion de un query update
    def execute_query_update(self, query):      
        try: 
            data = self.connection.execute(query)
            if data.rowcount != 0:
                result = True, data.rowcount, data.lastrowid
            else:
                result = False, 0, 0
        except Exception as e:
            raise        
        return result

    # Metodo para ejecucion de un query select
    def execute_query_selective(self, query):      
        try: 
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise

        return result


    # Metodo para la desconexion de la base de datos
    def disconnect(self):
        try:
            result = self.connection.close()
        except Exception as error:
            result = error.message
                
        return result
        