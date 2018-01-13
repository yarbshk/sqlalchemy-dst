# SQLAlchemy Dictionary Serialization Tools

SQLAlchemy DST is a set of must have functions and classes for working with the dictionary serialisation. It allows you to quickly convert a SQLAlchemy model to a python dictionary and vise versa. 

Why use it? Well, for example, I use this tools to reduce amount of requests to a database. So, this is a simple kind of caching complex objects in a session.

## Requirements
This module successfully passed unit testing on [Debian Jessie](https://wiki.debian.org/DebianJessie) with **Python 2.7** and **3.5** versions.

Depends on the following packages (see `requirements.txt`):
- [sqlalchemy](https://www.sqlalchemy.org/) >= 0.9.4

## Installation
This module is available as [PyPi package](https://pypi.python.org/pypi/sqlalchemy-dst), therefore you can install one as follows:

```bash
$ pip install sqlalchemy-dst
```

## Getting started

SQLAlchemy DST use only two functions (`row2dict()` and `dict2row()`) for serializing. Let's see how it works...

Imagine you have a User model with several relations (Role, Permissions), most likely, you will want to store instance of the model in a web server session for efficency purposes. Unfortunatelly, it's not possible to store instances of Python classes in the session. So, you need to **serialize** one **into a dictionary** first:
```python
>>> from sqlalchemy_dst import row2dict
>>> from tests.main import db
>>> from tests.schema import Permission, Role, User
>>> user = db.session.query(User).first()
```
Basic usage (one-dimensional dictionary):
```python
>>> row2dict(user)
{'password': 'x', '_secret': 'x', 'id': 1, 'role': None, 'role_id': 1, 'username': 'yarbshk'}
```
Advanced usage (three-dimensional dictionary without specific columns)
```python

>>> row2dict(user, depth=3, exclude_pk=True, exclude_underscore=True)
{'password': 'x', 'role': {'description': None, 'permissions': [{'name': 'posts:r', 'roles': [], 'id': 1}, {'name': 'posts:w', 'roles': [], 'id': 2}], 'users': [{'password': 'x', 'role': None, 'username': 'yarbshk', 'id': 1}], 'name': 'Moderator', 'id': 1}, 'username': 'yarbshk', 'id': 1}
```
Cheated usage (completely "clean" three-dimensional dictionary)
```python
>>> user_dict = row2dict(user, depth=3, exclude=['roles', 'users'], exclude_pk=True, exclude_underscore=True)
>>> user_dict
{'password': 'x', 'role': {'description': None, 'permissions': [{'name': 'posts:r', 'id': 1}, {'name': 'posts:w', 'id': 2}], 'name': 'Moderator', 'id': 1}, 'username': 'yarbshk', 'id': 1}
```
Great! Variable `user_dict` contains desirable value – dictionary.

Suppose in other part of the application you need to **deserialize that dictionary** to be able to use all features of the User's model (e.g. calling methods, querying data):
```python
>>> dict2row(user_dict, User)
<User (transient 139927902911456)>
```
The example above will create new instance of the User model (without any relations) to work with.

To create user's instance with all relations it's necessary to explicitly specify model classes (Role, Permission) of the used relations:
```python
>>> user_row = dict2row(user_dict, User, rel={'role': Role, 'permissions': Permission})
<User (transient 139927902904272)>
```
Well, now you are able to do any manipulations with this instance in the same way as before serialization:
```python
>>> [p.name for p in user_row.role.permissions]
['posts:r', 'posts:w']
```

Awesome, isn't it? :)

Arguments of the `dict2row()` method which left unnoticed (exclude, exclude_pk, exclude_underscore) works as same as in the `row2dict()` method.

## Pay attention

There are a few important things which can bring some troubles if you not sufficiently close with ones:

- Use suffix `_id` for foreign keys when you declare ones in your models (in other case the `exclude_pk` argument will not work at all).
- If you want to exclude some attribute of model which has synonym (and vice versa) you MUST exclude both attribute and synonym (in other case SQLAlchemy automatically sets the same value for attribute and their synonym even if one of them is excluded).

## Documentation

> Note that **default values** of the optional arguments in methods below **are setting implicitly**. This behavior is required by class DictionarySerializableModel (see detailed explanation below).

### row2dict(row, depth=None, exclude=None, exclude_pk=None, exclude_underscore=None)

Recursively walk row attributes to serialize ones into a dict.

- **row** (required) – _instance_ of the declarative base class (base SQLAlchemy model).
- **depth** (optional, default: `1`) – _number_ that represent the depth of related relationships.
- **exclude** (optional, default: `[]`) – _list_ of attributes names to exclude.
- **exclude_pk** (optional, default: `False`) – _are_ foreign keys (e.g. fk_name_id) excluded.
- **exclude_underscore** (optional, default: `False`) – _are_ private and protected attributes excluded.

### dict2row(d, model, rel=None, exclude=None, exclude_pk=None, exclude_underscore=None)

Recursively walk dict attributes to serialize ones into a row.

- **d** (required) – _dict_ which represent a serialized row.
- **model** (required) – _class_ nested from the declarative base class.
- **rel** (optional, default: `{}`) – _dict_ of key (relationship name) -value (class) pairs.
- **exclude** (optional, default: `[]`) – _list_ of attributes names to exclude.
- **exclude_pk** (optional, default: `False`) – _are_ foreign keys (e.g. fk_name_id) excluded.
- **exclude_underscore** (optional, default: `False`) – _are_ private and protected attributes excluded.

### DictionarySerializableModel

Class that extends serialization functionality of your models.

- **as_dict**(**kwargs) – wrapper around the `row2dict()` method – where _kwargs_ are mapped optional arguments for the `row2dict()` method. 
- **from_dict**(d, **kwargs) – wrapper around the `dict2row()` method – where _d_ is source dictionary, _kwargs_ are mapped optional arguments for the `dict2row()` method.
- **\_\_iter\_\_**() – object that can be iterated upon (it uses dictionary serialized by the `row2dict()` method).

Use it as a base class for the `sqlalchemy.ext.declarative_base()` method (try to explore the `cls` argument in depth).

If you decide to use the `DictionarySerializableModel` class as a base model, you may keep frequently used arguments values of the serialization methods in your model(s). Just set some or all of the following attributes in your model(s) as follows in example:

```python
from tests.main import db
...
class User(db.Model):
    _sa_dst_depth = 2
    _sa_dst_exclude = ['users']
    _sa_dst_exclude_pk = True
    _sa_dst_exclude_underscore = True
    _sa_dst_rel = {'role': Role}
    ...
```
```python
>>> from tests.main import db
>>> from tests.schema import User
>>> user = db.session.query(User).first()
>>> user.as_dict() # analog of row2dict(user, depth=2, exclude=['users'], exclude_pk=True, exclude_underscore=True)
{'password': 'x', 'role': {'description': None, 'permissions': [], 'name': 'Moderator', 'id': 1}, 'username': 'yarbshk', 'id': 1}
```

You can see an example of instantiating Flask + SQLAlchemy (with `DictionarySerializableModel`) in the `tests/main.py` file. 

## Copyright and License
Copyright (c) 2018 Yuriy Rabeshko. Code released under the MIT license.
