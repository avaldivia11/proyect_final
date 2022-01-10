from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()




class User(db.Model):
    __tablename__ = "users"
    id= db.Column(db.Integer, primary_key=True)
    rut= db.Column(db.String(200), unique=True)
    password= db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    roles= db.relationship('Role', secondary='roles_users')
    profile= db.relationship('Profile', backref='user', uselist=False)
    supervisiones=db.relationship('Supervision', backref='user')

    def serialize(self):
        return{
            "id":self.id,
            "rut":self.rut,
            "active":self.active,
            "profile":{
                "names":self.profile.names,
                "mother_lastname":self.profile.mother_lastname,
                "father_lastname":self.profile.father_lastname,
                "rut":self.profile.rut,
                "region":self.profile.region,
                "email":self.profile.email,
                "rol":self.profile.rol,
                "phone":self.profile.phone
            }
        }
    
    def serialize_with_roles(self):
        return{
            "id":self.id,
            "rut":self.rut,
            "active":self.active,
            "roles":self.get_roles(),
            "profile":{
                "names":self.profile.names,
                "mother_lastname":self.profile.mother_lastname,
                "father_lastname":self.profile.father_lastname,
                "rut":self.profile.rut,
                "region":self.profile.region,
                "email":self.profile.email,
                "rol":self.profile.rol,
                "phone":self.profile.phone
            }
        }

    def get_roles(self):
        return list(map(lambda role: role.serialize(), self.roles))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Profile(db.Model):
    __tablename__ = "profiles"
    id= db.Column(db.Integer, primary_key=True)
    names= db.Column(db.String(200))
    mother_lastname= db.Column(db.String(200))
    father_lastname= db.Column(db.String(200))
    rut= db.Column(db.String(200), nullable=False, unique=True)
    password= db.Column(db.String(200))
    region= db.Column(db.String(200))
    email= db.Column(db.String(200), nullable=False, unique=True)
    rol= db.Column(db.String(200))
    phone= db.Column(db.String(200))
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))

    def serialize(self):
        return{
            "id":self.id,
            "names":self.names,
            "mother_lastname":self.mother_lastname,
            "father_lastname":self.father_lastname,
            "rut":self.rut,
            "region":self.region,
            "email":self.email,
            "rol":self.rol,
            "phone":self.phone
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Role(db.Model):
    __tablename__ = "roles"
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable= False, unique=True)
    users= db.relationship('User', secondary='roles_users', backref='role')

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
        }

    def get_users(self):
        return list(map(lambda user: user.serialize(),self.users))
    
    def serialize_with_users(self):
        return{
            "id":self.id,
            "name":self.name,
            "users": []
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class RoleUser(db.Model):
    __tablename__ = "roles_users"
    role_id= db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

class Pauta(db.Model):
    __tablename__= "pautas"
    id= db.Column(db.Integer, primary_key=True)
    categoria= db.Column(db.String(200), unique=True)
    

    def serialize(self):
        return{
            "id":self.id,
            "categoria":self.categoria,
        }



    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Requerimiento(db.Model):
    __tablename__= "requerimientos"
    id= db.Column(db.Integer, primary_key=True)
    content= db.Column(db.Text(500))
    seleccion= db.Column(db.Boolean, default=False)
    pauta_id= db.Column(db.Integer, db.ForeignKey('pautas.id'))

    def serialize(self):
        return{
            "id":self.id,
            "content":self.content,
            "seleccion":self.seleccion,
            "pauta_id":self.pauta_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Resultado(db.Model):
    __tablename__= "resultados"
    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(250), nullable=False)
    content= db.Column(db.Text(500))
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    supervision_id= db.Column(db.Integer, db.ForeignKey('supervisiones.id'))
    requerimiento_id= db.Column(db.Integer, db.ForeignKey('requerimientos.id'))

    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "created_at":self.created_at,
            "supervision_id":self.supervision_id,
            "requerimiento_id":self.requerimiento_id
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Supervision(db.Model):
    __tablename__= "supervisiones"
    id= db.Column(db.Integer, primary_key=True)
    content= db.Column(db.Text(500))
    title= db.Column(db.String(500))
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    resultados= db.relationship('Resultado', backref='supervision')

    def serialize(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "created_at":self.created_at,
            "user_id":self.user_id
        }

    def serialize_with_resultados(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content,
            "created_at":self.created_at,
            "user_id":self.user_id,
            "resultados": list(map(lambda resultado: resultado.serialize(), self.resultados))
        }

    def get_resultados(self):
        return list(map(lambda resultado: resultado.serialize(), self.resultados))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

