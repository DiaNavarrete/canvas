from sql_client import SQLclient
from sqlalchemy import create_engine
import configparser
from flask import jsonify
from datetime import datetime

sql_client = SQLclient()

class Model:
    def __init__(self):
        self.config = load_config()
        self.sql_connect(self.config['DATABASE'])    
    
      # Metodo de conexion a sql
    def sql_connect(self, config):
        try:
            connector = config['CONNECTOR']
            user = config['USER']
            password = config['PASSWORD']
            host = config['HOST']
            port = config['PORT']
            database = config['NAME']
            sql_client.get_connect(connector,user, password, host, port, database)
            
        except Exception as error:
            print('ERROR', error.message)
            return False
    
        return True
    
    def get_default_boxes(self):
        query= '''SELECT * FROM standard_box'''
        result = sql_client.execute_query(query)
        return result

    def get_user_projects(self, current_user):
        query= "SELECT * FROM canvas_project WHERE username='{user}'".format(user=current_user)
        result = sql_client.execute_query(query)
        return result
    
    def get_project(self, project_id):
        query= "SELECT * FROM canvas_project WHERE ID='{id}'".format(id=project_id)
        result = sql_client.execute_query(query)
        return result[0]
    
    def get_canvas(self, project_id):
        query='''SELECT * FROM canvas_box LEFT JOIN standard_box on 
                canvas_box.standard_box_ID=standard_box.ID WHERE 
                canvas_box.canvas_project_ID={id}'''.format(id=project_id)
        result = sql_client.execute_query(query)
        return result

    def update_canvas(self, project_id, title):
        now = datetime.now()
        query='''UPDATE canvas_project SET last_modified_date="{last_modified}",
                   canvas_title="{canvas_title}" WHERE ID={id}'''.format(
                last_modified=now,  id=project_id, canvas_title=title  )
        saved, rowcount, id =sql_client.execute_query_update(query)
        return saved

    def create_canvas(self, user, project_name, canvas_title):
        user = to_unicode_or_bust(user)
        project_name = to_unicode_or_bust(project_name)
        canvas_title = to_unicode_or_bust(canvas_title)
        now = datetime.now()
        query= U'''INSERT INTO canvas_project 
            (username, creation_date, last_modified_date, project_name, canvas_title) VALUES
                ('{username}', '{creation_date}', '{last_modified}', '{name}', '{title}');'''.format(
                    username=user,
                    creation_date=now,
                    last_modified=now,
                    name=project_name,
                    title=canvas_title
                    )
        saved, rowcount, id = sql_client.execute_query_update(query)
        return saved, id 

    def create_canvas_box(self, project_id, data_boxes):
        data_insert=[]
        for box in data_boxes:
            row_data=(to_unicode_or_bust(box['box_text']),int(box['box_ID']), project_id)
            data_insert.append(row_data)
        query='INSERT INTO canvas_box (box_text, standard_box_ID, canvas_project_ID) VALUES {values}'.format(
                    values=str(data_insert)[1:-1])
        saved, rowcount, id = sql_client.execute_query_update(query)
        return saved, rowcount

    def update_canvas_box(self,  data_boxes):
        data_insert=[]
        for box in data_boxes:
            row_data=(to_unicode_or_bust(box['box_text']), int(box['box_ID']))
            data_insert.append(row_data)
        query='''INSERT INTO canvas_box (box_text,  ID) VALUES {values}
            ON DUPLICATE KEY UPDATE box_text=VALUES(box_text), ID=VALUES(ID)'''.format(
                    values=str(data_insert)[1:-1])
        saved, rowcount, id = sql_client.execute_query_update(query)
        return saved, rowcount

    def delete_canvas(self, project_id):
        id=int(project_id)
        query='DELETE FROM canvas_box WHERE canvas_project_ID={project_id}'.format(project_id=id)
        saved, rowcount, idel = sql_client.execute_query_update(query)
        if saved:
            query='DELETE FROM canvas_project WHERE ID={project_id}'.format(project_id=id)
            saved, rowcount, id = sql_client.execute_query_update(query)
            return saved
        return False


def to_unicode_or_bust(obj, encoding="latin1"):
    obj=str(obj).strip()
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj=unicode(obj, encoding)
    #print(obj)
    return str(obj)

# Metodo para cargar los datos del archivo de configuracion
def load_config( config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config