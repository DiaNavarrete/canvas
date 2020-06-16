from flask import Flask, request, render_template, redirect,url_for
from flask_restful import Api
from flask_cors import CORS, cross_origin
from model import Model, load_config
import json

app = Flask(__name__)
CORS(app, resources={r'/*': {"origins": "*"}},
     allow_headers=['Content-Type', "Access-Control-Allow-Credentials"])

model= Model()

@app.route('/',  methods=['GET'])
@cross_origin()
def home():
    return render_template("home.html")
    
@app.route('/user',  methods=['GET'])
@cross_origin()
def user():
    current_user = request.args.get('user')
    # traer lista de proyectos creados por el usuario
    projects_created = model.get_user_projects(current_user)    
    return render_template("index.html", user=current_user, projects=projects_created)

@app.route('/canvas',  methods=['GET'])
@cross_origin()
def view_canvas():
    current_user=request.args.get('user')
    project_id=request.args.get('id')
    #Se busca un proyecto
    if project_id!=None:
        data_project=model.get_project(project_id)
        current_user=data_project['username']
        box_data=model.get_canvas(project_id)
        box_data=[box_data[:3], box_data[3:6], box_data[6:]]
        return render_template("canvas.html", user=current_user, boxes=box_data, project=data_project)

    else: #se crea el proyecto
        box_data=model.get_default_boxes()
        box_data=[box_data[:3], box_data[3:6], box_data[6:]]
        return render_template("canvas.html", user=current_user, boxes=box_data)

@app.route('/canvas',  methods=['POST'])
@cross_origin()
def create_canvas():
    data=json.loads(request.get_data())
    # crear el proyecto canvas
    saved, project_id =model.create_canvas(data['user'], data['name'], data['title'])
    if saved:
        # Guardar los datos del canvas
        saved, rowcount= model.create_canvas_box(project_id, data['boxes'])
        if saved and rowcount==9:
            return url_for('user', user=data['user']), 200
    return '', 400

@app.route('/canvas',  methods=['PUT'])
@cross_origin()
def update_canvas():
    project_id=request.args.get('id')
    data=json.loads(request.get_data())
    # actualizar el proyecto canvas
    saved =model.update_canvas(project_id, data['title'])
    if saved:
        # actualizar los datos del canvas
        saved, rowcount= model.update_canvas_box(data['boxes'])
        if saved and rowcount==9:
            return url_for('user', user=data['user']), 200
    return '', 400

@app.route('/canvas',  methods=['DELETE'])
@cross_origin()
def delete_canvas():
    current_user=request.args.get('user')
    project_id=request.args.get('id')
    saved =model.delete_canvas(project_id)
    if saved:
        return url_for('user', user=current_user), 200
    return '', 400

