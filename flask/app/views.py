from typing import List, Dict
from flask_mysqldb import MySQL
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import mysql.connector
import json
import os
import base64
from flask import request, render_template, jsonify, Response, flash, redirect, url_for,jsonify
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, FileField, SelectField, PasswordField, SubmitField, validators, HiddenField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired, ValidationError, Optional
from werkzeug.utils import secure_filename
from app import app
import time
import glob
from werkzeug.datastructures import MultiDict
import hashlib
import json
import zipfile
import pathlib



types = ('*.png', '*.html', '*.jpg', '*.jpeg', '*.csv')
files_folder = "./app/static/files/"
files_folder2="./app/static/files/518d3db40a4689f9ba10b119f54c999281072570ae7953df9e2b698600c6df3c/"
files_container = "/output"

app.config['SECRET_KEY']="catalogos"
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'catalogos'
db = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

class User(UserMixin):

    def __init__(self, id, username, password, first_name, second_name, user_type) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.second_name = second_name
        self.user_type = user_type

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

class ModelUser():
    @classmethod
    def login(self, db, username, password):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_user, username, password, first_name, second_name, user_type FROM users WHERE username = '{}'""".format(username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                print("SIUx2")
                print("Siux2")
                print(row[2],password)
                print(type(password))
                print(type(row[2]))
                if(row[2] == password):
                    print("LLEGO")
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
                    return user
            return None
        except Exception as ex:
            raise Exception(ex)
        
        finally:
            print("SE CIERRA CURSOR")
            cursor.close()
            

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, first_name, second_name, user_type FROM users WHERE id_user = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3], row[4])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
        finally:
            cursor.close()
        


@login_manager.user_loader
def load_user(id_user):
    return ModelUser.get_by_id(db, id_user)

def conexion_db():
    conn = mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="catalogos"
    )
    return conn

##### AGREGAR CATALOGO EN AUTOMATICO PARA EJEMPLO
#def agregar_catalogo_ejemplo():
#    conn = conexion_db()
#    sql = "INSERT INTO catalogos (nombre_catalogo,descripcion_catalogo,archivo_catalogo,archivo_nombre,usuario_catalogo) VALUES (%s,%s,%s,%s,%s)"
#    cursor = conn.cursor()
#    with open("app/CV_MarianaHinojosa.pdf","rb") as pdf_file:
#        archivo_binario = pdf_file.read()
#
#    cursor.execute(sql, ("Catalogo Ejemplo","Descripcion ejemplo",archivo_binario,"archivo_ejemplo.pdf","admin",))
#    conn.commit()

#agregar_catalogo_ejemplo()

class CatalogoForm(FlaskForm):
    nombre = StringField('Nombre catálogo', validators=[InputRequired(),Length(min=10, max=100)])
    descripcion = TextAreaField('Descripcion catálogo',validators=[InputRequired(),Length(max=200)])
    archivo = FileField('Archivo catálogo')


class UsuarioForm(FlaskForm):
    usuario = StringField('Usuario', validators=[Email(message='Ingrese un correo valido'),DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    tipo = SelectField(u'Tipo Usuario', choices=[('1', 'Admin'), ('2', 'Normal')])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirmar = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password',message='Las contraseñas deben coincidir')])
    def validate_usuario(self, field):
        try:
            sql = """SELECT username FROM users WHERE username = '{}'""".format(field.data)
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                raise ValidationError('Ese usuario ya existe, elige uno diferente')
        finally:
            cursor.close()
            
            
def validate_same_username(form,field):
    if(form.usuario_compare.data != field.data):
        try:
            sql = """SELECT username FROM users WHERE username = '{}'""".format(field.data)
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                raise ValidationError('Ese usuario ya existe, elige uno diferente')
        finally:
            cursor.close()
            
                      
class UsuarioFormUpdate(FlaskForm):
    usuario = StringField('Usuario', validators=[Email(message='Ingrese un correo valido'),DataRequired(), validate_same_username])
    usuario_compare = HiddenField()
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    tipo = SelectField(u'Tipo Usuario', choices=[('1', 'Admin'), ('2', 'Normal')],default=2)
    password = PasswordField('Contraseña', validators=[Optional(), EqualTo('confirmar',message='Las contraseñas deben coincidir')])
    confirmar = PasswordField('Confirmar Contraseña', validators=[Optional(), EqualTo('password',message='Las contraseñas deben coincidir')])
        
        
        
 
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('catalogos')) 
    return render_template('home.html')
    
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/adminlte')
def admin():
    return render_template('adminlte.html')
    
@app.route('/join', methods=['POST'])
def my_form_post():
    nombre_usuario = request.form['text1']
    password_usuario = request.form['text2']
    password = hashlib.md5((password_usuario+app.config['SECRET_KEY']).encode()).hexdigest()
    user = ModelUser.login(db,nombre_usuario, password)
    if(user):
        login_user(user)
        return redirect(url_for('catalogos'))    
    return render_template('home.html',error="Usuario y/o contraseña incorrecta")


@app.route('/agregar_catalogo', methods=['POST','GET'])
@login_required
def agregar_catalogo():
    form = CatalogoForm()
    if request.method == 'POST':
        if form.validate_on_submit() and form.validate():
            try:
                nombre_catalogo = form.nombre.data
                descripcion_catalogo = form.descripcion.data
                file = request.files['file']
                archivo_binario = file.read()
                archivo_nombre = secure_filename(file.filename)
                sql = "INSERT INTO catalogs (catalog_name,catalog_description,file,filename,id_user) VALUES (%s,%s,%s,%s,%s)"
                cursor = db.connection.cursor()
                cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,archivo_binario,archivo_nombre,current_user.id,))
                db.connection.commit()
                print("se guardo!!!!")
                return redirect(url_for('catalogos'))
            except Exception as ex:
                raise Exception(ex)
            finally:
                cursor.close()     
    return render_template('agregar_catalogo.html', form=form)

@app.route('/agregar_usuario', methods=['POST','GET'])
@login_required
def agregar_usuario():
    form = UsuarioForm()
    if form.validate_on_submit() and form.validate():
        try:
            usuario = form.usuario.data
            nombre = form.nombre.data
            apellido = form.apellido.data
            password = hashlib.md5((form.password.data+app.config['SECRET_KEY']).encode()).hexdigest()
            confirmar = hashlib.md5((form.confirmar.data+app.config['SECRET_KEY']).encode()).hexdigest()
            tipo_usuario = form.tipo.data
            sql = "INSERT INTO users (username,first_name,second_name,password,user_type) VALUES (%s,%s,%s,%s,%s)"
            cursor = db.connection.cursor()
            cursor.execute(sql, (usuario,nombre,apellido,password,tipo_usuario,))
            db.connection.commit()
            return redirect(url_for('usuarios'))
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()   
    return render_template('agregar_usuario.html', form=form)

@app.route('/getFile', methods=['GET'])
def getFile():
    try:
        select_catalogo = "SELECT file, filename FROM catalogs WHERE id_catalog = {}".format(request.args.get('id'))
        cursor = db.connection.cursor()
        cursor.execute(select_catalogo)
        myresult = cursor.fetchone()
        print(myresult[1])
        filename,extension = os.path.splitext(myresult[1])
        print(extension)
        print(filename)
        return Response(myresult[0], mimetype="text/"+extension, headers={"Content-disposition": "attachment; filename="+filename+"."+extension})
    except Exception as ex:
        raise Exception(ex)
    finally:
        cursor.close()
    return None

@app.route('/dynamic_panel', methods=['GET'])
def dynamic_panel():
    return render_template('dynamic_panel.html')


@app.route('/dynamic_panel_2', methods=['GET'])
def dynamic_panel_2():
    with open('app/filters_2.json', 'r') as f:
        data = json.load(f)
    levels = [data["levels"]["1"]["name"], data["levels"]["2"]["name"],data["levels"]["3"]["name"]]
    data = data["levels"]["1"]["values"].keys()
    return render_template('dynamic_panel_2.html', data=data, levels=levels)

@app.route('/dynamicPanel', methods=['GET'])
def dynamicPanel():
    with open('app/cod_Cancer.json', 'r') as f:
        data2 = json.load(f)
    with open('app/filters_2.json', 'r') as f:
        data = json.load(f)
    levels = [data["levels"]["1"]["name"], data["levels"]["2"]["name"],data["levels"]["3"]["name"]]
    data = data["levels"]["1"]["values"].keys()
    return render_template('dynamicPanel.html', data=data,data2=data2, levels=levels)

@app.route('/get_json', methods=['GET'])
def get_json():
    label = request.args.get('label')
    level = request.args.get('level')
    with open('app/filters_2.json', 'r') as f:
        data = json.load(f)
    if(level=="1"):
        #print(label)
        print(data["levels"]["1"]["values"][label])
        children = data["levels"]["1"]["values"][label]["childrens"]['2']
        names = []
        level_2 = data["levels"]["2"]["values"]
        for key in level_2:
            id = level_2[key]['id']
            if(id in children):
                names.append(level_2[key]['name'])
        print(names)
        return names 
       
    if(level=="2"):
        #print(label)
        print(data["levels"]["2"]["values"][label])
        children = data["levels"]["2"]["values"][label]["childrens"]['3']
        names = []
        level_3 = data["levels"]["3"]["values"]
        for key in level_3:
            id = level_3[key]['id']
            if(id in children):
                names.append(level_3[key]['name'])
        return names                   
    else:
        return data[0][labels[0]][0][labels[1]]

            
@app.route('/get_panels', methods=['GET'])
def get_panels():

    paths = request.args.getlist('paths[]')
    print(paths)
    #time.sleep(2)
    total_files = []
    for x_label in paths:
        code, x_path, x_path_extracted = checkOutputType(files_folder+x_label+"/")
        if(code == 1):
            try:
                with zipfile.ZipFile(x_path_extracted, 'r') as zip_ref:
                    zip_ref.extractall(x_path)
            except:
                print("NO EXISTE EL ZIP")
        
        for files in types:
            total_files.extend(sorted( filter( os.path.isfile, glob.glob(x_path + files) ) ))

    total_files = [file.split("./app")[1] for file in total_files]
    print(total_files)
            
    result = {"total_files":len(total_files), "paths":total_files}
    


    return (result,200)

    


def checkOutputType(path):
    print("CHECK OUTPUT")
    zip_files = (glob.glob(path+"*.zip"))
    if(len(zip_files) > 0):
        print("HAY UN ZIP")
        filepath = zip_files[0].split(".zip")[0]
        if(os.path.exists(filepath)):
            print("LA RUTA YA EXISTE, NO ES NECESARIO DESCOMPRIMIR")
            print(filepath)
            return [0,filepath+"/", None]
        else:
            print("LA RUTA NO EXISTE, ES NECESARIO DESCOMPRIMIR")
            print(filepath)
            filepath_zip = filepath+".zip"
            return [1,filepath+"/", filepath_zip]
    print("NO HAY CARPETA CONTENEDORA")
    print(path)
    return [0,path, None]

@app.route('/catalogos')
@login_required
def catalogos():
    try:
        select_usuarios = "SELECT id_catalog,catalog_name,catalog_description FROM catalogs where id_user = {}".format(current_user.id)
        cursor = db.connection.cursor()
        cursor.execute(select_usuarios)
        result = cursor.fetchall()
        return render_template('catalogos2.html',data=result)
    except Exception as ex:
        raise Exception(ex)
    finally:
        cursor.close()
        


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/usuarios')
@login_required
def usuarios():
    if(current_user.user_type == 1):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_user, username, first_name, second_name FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template('usuarios2.html',data=result)
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
    
    return redirect(url_for('catalogos'))

@app.route('/actualizar_usuario', methods=['GET', 'POST'])
@login_required
def actualizar_usuario():
    if(current_user.user_type == 1):
        id_user = request.args.get('id')
        form = UsuarioFormUpdate()
        if(request.method =='GET'):
            try:
                select_catalogo = "SELECT id_user, username, first_name, second_name, user_type FROM users WHERE id_user = {}".format(id_user)
                cursor = db.connection.cursor()
                cursor.execute(select_catalogo)
                result = cursor.fetchone()
                print(result)
                form.usuario.data = result[1]
                form.usuario_compare.data = result[1]
                form.nombre.data = result[2]
                form.apellido.data = result[3]
                form.tipo.process_data(result[4]) 
            except Exception as ex:
                raise Exception(ex)
            finally:
                cursor.close()
                
        if form.validate_on_submit():
            try:
                usuario = form.usuario.data
                nombre = form.nombre.data
                apellido = form.apellido.data
                tipo = form.tipo.data
                password = form.password.data
                confirmar = form.confirmar.data
                cursor = db.connection.cursor()
                sql = ""        
                if password !='' and confirmar != '':
                    password = hashlib.md5((form.password.data+app.config['SECRET_KEY']).encode()).hexdigest()
                    sql = "UPDATE users SET username = %s, first_name = %s, second_name = %s, user_type = %s, password = %s where id_user = %s"
                    cursor.execute(sql, (usuario,nombre,apellido,tipo,password, id_user,))    
                else:
                    sql = "UPDATE users SET username = %s, first_name = %s, second_name = %s, user_type = %s where id_user = %s"
                    cursor.execute(sql, (usuario,nombre,apellido,tipo, id_user,))
                db.connection.commit()
                return redirect(url_for('usuarios'))
            except Exception as ex:
                raise Exception(ex)
            finally:
                cursor.close()
                
        return render_template('actualizar_usuario.html',form=form)
    return redirect(url_for('catalogos'))


@app.route('/borrar_usuario', methods=['GET'])
@login_required
def borrar_usuario():
    
    if(current_user.user_type == 1):
        print(request.args.get('id'))
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM users WHERE id_user = {}".format(request.args.get('id'))
            cursor.execute(sql)
            db.connection.commit()
            return redirect(url_for('usuarios'))
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
    return ('', 204)

@app.route('/actualizar_catalogo', methods=['GET','POST'])
@login_required
def get_catalogo():
    form = CatalogoForm()
    id_catalog = request.args.get('id')
    print(id_catalog)
    if(request.method =='GET'):
        try:
            select_catalogo = "SELECT id_catalog, catalog_name, catalog_description FROM catalogs WHERE id_catalog = {}".format(id_catalog)
            cursor = db.connection.cursor()
            cursor.execute(select_catalogo)
            result = cursor.fetchone()
            print(result)
            form.nombre.data = result[1]
            form.descripcion.data = result[2]
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
            
    if form.validate_on_submit():
        try:
            nombre_catalogo = form.nombre.data
            descripcion_catalogo = form.descripcion.data
            file = request.files['file']
            cursor = db.connection.cursor()        
            if file.filename !='':
                file = request.files['file']
                archivo_binario = file.read()
                archivo_nombre = secure_filename(file.filename)
                sql = "UPDATE catalogs SET catalog_name = %s, catalog_description = %s, file = %s, filename = %s where id_catalog = %s"
                cursor.execute(sql, (nombre_catalogo,descripcion_catalogo, archivo_binario, archivo_nombre, id_catalog,))
                db.connection.commit()
            else:
                sql = "UPDATE catalogs SET catalog_name = %s, catalog_description = %s where id_catalog = %s"
                cursor.execute(sql, (nombre_catalogo,descripcion_catalogo,id_catalog,))
                db.connection.commit()
            return redirect(url_for('catalogos'))
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()
            
    return render_template('actualizar_catalogo.html',form=form)



@app.route('/borrar_catalogo', methods=['GET'])
@login_required
def borrar_catalogo():
    
    print(request.args.get('id'))
    try:
        cursor = db.connection.cursor()
        sql = "DELETE FROM catalogs WHERE id_catalog = {}".format(request.args.get('id'))
        cursor.execute(sql)
        db.connection.commit()
        return redirect(url_for('catalogos'))
    except Exception as ex:
        raise Exception(ex)
    finally:
            cursor.close()
    return ('', 204)
    

        