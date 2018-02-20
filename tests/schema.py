from .main import db


class User(db.Model):
    __tablename__ = 'users'

    _secret = db.synonym('password')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    role = db.relationship('Role', back_populates='users')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


role_permissions = db.Table('role_permissions', db.Model.metadata,
    db.Column('role_id', db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.ForeignKey('permissions.id'), primary_key=True)
)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    permissions = db.relationship('Permission',
                                  back_populates='roles',
                                  secondary=role_permissions)
    users = db.relationship('User', back_populates='role')


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    roles = db.relationship('Role',
                            back_populates='permissions',
                            secondary=role_permissions)
