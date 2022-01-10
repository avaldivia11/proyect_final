import datetime
from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Profile, Role, RoleUser, Pauta, Requerimiento, Resultado, Supervision


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '455a0595071af6e2385c0ec556cb329c'
db.init_app(app)
Migrate(app, db) #db init, db migrate, db upgrade, db downgrade
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api/users', methods=['GET', 'POST'])
@app.route('/api/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id= None):
    if request.method == 'GET':
        if id is not None:
            users= User.query.get(id)
            if not users: return jsonify({"msg": "Usuario no encontrado"}), 404
            return jsonify(users.serialize()), 200
        else:
            users= User.query.all()
            users=list(map(lambda user: user.serialize_with_roles(),users))
            return jsonify(users), 200

    if request.method == 'POST':
        rut= request.json.get("rut")
        password= request.json.get("password")
        names= request.json.get("names", "")
        mother_lastname= request.json.get("mother lastname", "" )
        father_lastname= request.json.get("father lastname", "" )
        region= request.json.get("region", "")
        email= request.json.get("email")
        roles= request.json.get("roles", [2])
        phone= request.json.get("phone")

        user_exist = User.query.filter_by(rut=rut).first()
        if user_exist: return jsonify({"error": "el usuario ya existe!"}), 400

        user = User()
        user.rut = rut
        user.password = generate_password_hash(password)
        user.active = True
        
        
        profile = Profile()
        profile.names = names
        profile.rut = rut
        profile.mother_lastname = mother_lastname
        profile.father_lastname = father_lastname
        profile.region = region
        profile.email = email
        profile.phone = phone
        #profile.user_id = user.id
        #profile.save()

        for role in roles:
            role= Role.query.get(role)
            user.roles.append(role)

        user.profile= profile
        user.save()

        return jsonify(user.serialize_with_roles()), 201
    
    if request.method == 'PUT':
        rut= request.json.get("rut")
        password= request.json.get("password")
        names= request.json.get("names", "")
        mother_lastname= request.json.get("mother lastname", "" )
        father_lastname= request.json.get("father lastname", "" )
        region= request.json.get("region", "")
        email= request.json.get("email")
        roles= request.json.get("roles", [2])
        phone= request.json.get("phone")
        
        if not rut: return jsonify ({"msg": "El rut es requerido"}), 400
        if not password: return jsonify ({"msg": "La contraseña es requerida"}), 400

        user = User.query.get(id)
        if not user: return jsonify({"msg": "El usuario no existe"}), 404

        user.rut = rut
        user.password = generate_password_hash(password)
        user.active = True
        profile = Profile.query.get(id)
        profile.names = names
        profile.rut = rut
        profile.mother_lastname = mother_lastname
        profile.father_lastname = father_lastname
        profile.region = region
        profile.email = email
        profile.phone = phone
        #profile.user_id = user.id
        #profile.save()

        for role in roles:
            role= Role.query.get(role)
            user.roles.append(role)

        user.profile= profile
        
        user.update()

        return jsonify(user.serialize_with_roles()), 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user: return jsonify({"msg": "El usuario no existe"}), 404

        user.delete()

        return jsonify({"success": "El usuario fue eliminado"}),200

@app.route("/api/login", methods=['POST'])
def login():
        rut= request.json.get("rut")
        password= request.json.get("password")
        names= request.json.get("names", "")
        mother_lastname= request.json.get("mother lastname", "" )
        father_lastname= request.json.get("father lastname", "" )
        region= request.json.get("region", "")
        email= request.json.get("email")
        roles= request.json.get("roles", [2])
        phone= request.json.get("phone", "")

        user_exist = User.query.filter_by(rut=rut).first()

        
        if not user_exist: return jsonify({"msg": "rut/password son incorrectos"}), 400

        if not check_password_hash(user_exist.password, password):
            return jsonify({"msg": "rut/password son incorrectos"}), 400

        expires = datetime.timedelta(days=1)

        accesses_token = create_access_token(identity=user_exist.id, expires_delta = expires)

        data = {
            "access_token": accesses_token,   
            "user": user_exist.serialize()
        }

        return jsonify(data),200

@app.route("/api/register", methods=['POST'])
def register():
    if request.method == 'POST':
        rut= request.json.get("rut")
        password= request.json.get("password")
        names= request.json.get("names", "")
        mother_lastname= request.json.get("mother lastname", "" )
        father_lastname= request.json.get("father lastname", "" )
        region= request.json.get("region", "")
        email= request.json.get("email")
        roles= request.json.get("roles", [2])
        phone= request.json.get("phone")

        user_exist = User.query.filter_by(rut=rut).first()
        if user_exist: return jsonify({"error": "el usuario ya existe!"}), 400

        user = User()
        user.rut = rut
        user.password = generate_password_hash(password)
        user.active = True
        
        
        profile = Profile()
        profile.names = names
        profile.rut = rut
        profile.mother_lastname = mother_lastname
        profile.father_lastname = father_lastname
        profile.region = region
        profile.email = email
        profile.phone = phone
        #profile.user_id = user.id
        #profile.save()

        for role in roles:
            role= Role.query.get(role)
            user.roles.append(role)

        user.profile= profile
        user.save()
    

        if not user: jsonify({"msg": "Registro fallido"}), 400

        expires = datetime.timedelta(days=1)

        accesses_token = create_access_token(identity=user.id, expires_delta = expires)

        data = {
            "access_token": accesses_token,
            "user": user.serialize()
        }

        return jsonify(data),200

@app.route("/api/profile", methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify(user.serialize()), 200


@app.route("/api/pautas", methods=['GET', 'POST'])
@app.route('/api/pautas/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def pautas(id=None):
    if request.method == 'GET':
        if id is not None:
            pautas= Pauta.query.get(id)
            if not pautas: return jsonify({"msg": "Pauta no encontrada"}), 404
            return jsonify(pautas.serialize()), 200
        else:
            pautas= Pauta.query.all()
            pautas=list(map(lambda categoria: categoria.serialize(),pautas))
            return jsonify(pautas), 200


    if request.method == 'POST':
        pautas= request.json.get("categoria")


        pauta=Pauta()
        pauta.categoria = pautas
        pauta.save()

        return jsonify(pautas), 200
    
    if request.method == 'PUT':


        categoria = request.json.get("categoria")

        pautas = Pauta.query.get(id)
        if not pautas: return jsonify({"msg": "La pauta no existe"}), 404

        pautas.categoria = categoria
        pautas.update()
        return jsonify(pautas.serialize()), 200

    if request.method == 'DELETE':
        pautas = Pauta.query.get(id)
        if not pautas: return jsonify({"msg": "La pauta no existe"}), 404

        pautas.delete()

        return jsonify({"success": "La pauta fue eliminada"}),200

@app.route("/api/requerimientos", methods=['GET', 'POST'])
@app.route('/api/requerimientos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def requerimientos(id=None):
    if request.method == 'GET':
        if id is not None:
            requerimientos= Requerimiento.query.get(id)
            if not requerimientos: return jsonify({"msg": "Requerimiento no existe"}), 404
            return jsonify(requerimientos.serialize()), 200
        else:
            requerimientos= Requerimiento.query.all()
            requerimientos=list(map(lambda requerimiento: requerimiento.serialize(),requerimientos))
            return jsonify(requerimientos), 200

    if request.method == 'POST':
        content= request.json.get("content")
        seleccion= request.json.get("seleccion")
        pauta_id= request.json.get("pauta_id")

        requerimiento=Requerimiento()
        requerimiento.content = content
        requerimiento.save()

        return jsonify(requerimiento.serialize()), 200

    if request.method == 'PUT':
        content= request.json.get("content")
        seleccion= request.json.get("seleccion")
        pauta_id= request.json.get("pauta_id")

        requerimientos = Requerimiento.query.get(id)
        if not requerimientos: return jsonify({"msg": "El requerimiento no existe"}), 404

        requerimientos.content = content
        requerimientos.seleccion = seleccion
        requerimientos.update()
        return jsonify(requerimientos.serialize()), 200

    if request.method == 'DELETE':
        requerimientos = Requerimiento.query.get(id)
        if not requerimientos: return jsonify({"msg": "El requerimiento no existe"}), 404

        requerimientos.delete()

        return jsonify({"success": "El requerimiento fue eliminado"}),200

@app.route("/api/roles", methods=['GET', 'POST'])
@app.route('/api/roles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def roles(id=None):
    if request.method == 'GET':
        if id is not None:
            roles= Role.query.get(id)
            if not roles: return jsonify({"msg": "Rol no existe"}), 404
            return jsonify(roles.serialize()), 200
        else:
            roles= Role.query.all()
            roles=list(map(lambda role: role.serialize(),roles))
            return jsonify(roles), 200


    if request.method == 'POST':
        name= request.json.get("name")


        roles=Role()
        roles.name = name
        roles.save()

        return jsonify(roles.serialize()), 200

    if request.method == 'PUT':
        name= request.json.get("name")

        roles = Role.query.get(id)
        if not roles: return jsonify({"msg": "El rol no existe"}), 404

        roles.name = name
        roles.update()
        return jsonify(roles.serialize()), 200

    if request.method == 'DELETE':
        roles = Role.query.get(id)
        if not roles: return jsonify({"msg": "El rol no existe"}), 404

        roles.delete()

        return jsonify({"success": "El rol fue eliminado"}),200

@app.route("/api/resultados", methods=['GET', 'POST'])
@app.route('/api/resultados/<int:id>', methods=['GET', 'DELETE'])
def resultados(id=None):

    if request.method == 'GET':
        if id is not None:
            resultados= Resultado.query.get(id)
            if not resultados: return jsonify({"msg": "Resultado no encontrado"}), 404
            return jsonify(resultados.serialize()), 200
        else:
            resultados= Resultado.query.all()
            resultados=list(map(lambda resultado: resultado.serialize(),resultados))
            return jsonify(resultados), 200

    if request.method == 'POST':
        title= request.json.get("title")
        content= request.json.get("content")
        created_at= request.json.get("created_at")


        resultados=Resultado()
        resultados.title = title
        resultados.content= content
        resultados.created_at= created_at
        resultados.save()

        return jsonify(resultados.serialize()), 200

    if request.method == 'PUT':
        title= request.json.get("title")
        content= request.json.get("content")
        created_at= request.json.get("created_at")

        resultados = Resultado.query.get(id)
        if not resultados: return jsonify({"msg": "El Resultado que intenta consultar no existe"}), 404

        resultados=Resultado()
        resultados.title = title
        resultados.content= content
        resultados.created_at= created_at
        resultados.update()

        return jsonify(resultados.serialize()), 200

    if request.method == 'DELETE':
        resultados = Resultado.query.get(id)
        if not resultados: return jsonify({"msg": "El Resultado que intenta consultar no existe"}), 404

        resultados.delete()
        return jsonify({"success": "Los resultados han sido eliminados con exito"}),200


@app.route("/api/supervisiones", methods=['GET', 'POST'])
@app.route('/api/supervisiones/<int:id>', methods=['GET', 'DELETE'])
def supervisiones(id=None):
    if request.method == 'GET':
        if id is not None:
            supervisiones= Supervision.query.get(id)
            if not supervisiones: return jsonify({"msg": "Supervision no encontrada"}), 404
            return jsonify(supervisiones.serialize()), 200
        else:
            supervisiones= Supervision.query.all()
            supervisiones=list(map(lambda supervision: supervision.serialize(),supervisiones))
            return jsonify(supervisiones), 200

    if request.method == 'POST':
        
        content= request.json.get("content")
        title= request.json.get("title")
        created_at= request.json.get("created_at")
        resultados= request.json.get("resultados", "")


        supervisiones=Supervision()
        supervisiones.content= content
        supervisiones.title = title
        supervisiones.created_at= created_at
        supervisiones.save()

        for resultado in resultados:
            resultado= Resultado.query.get(resultado)
            supervision.resultados.append(resultado)

        supervisiones.save()

        return jsonify(supervisiones.serialize_with_resultados()), 200


if __name__ == '__main__':
    app.run()