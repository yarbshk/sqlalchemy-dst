# SQLAlchemy Dictionary Serialization Tools

SQLAlchemy DST is a set of must have functions and classes for the dictionary serialisation. It allows you to quickly convert a SQLAlchemy model to a python dictionary and vise versa. 

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

SQLAlchemy DST use only two functions (`row2dict()` and `dict2row()`) to serialize objects. Let's see how it works...

Imagine you have a User model with several relations (Role, Permissions), most likely, you will want to store instance of the model in a web server session for efficency purposes. Unfortunatelly, it's not possible to store instances of Python classes in the session. So, you need to **serialize** one **into a dictionary** first:
```python
>>> from sqlalchemy_dst import dict2row, row2dict
>>> from tests.main import db
>>> from tests.schema import Permission, Role, User
>>> user = db.session.query(User).first() # create an instance of the User model
```
Serialize the instance of the User model into the one-dimensional dictionary:
```python
>>> row2dict(user)
{'username': 'yarbshk', 'role': None, 'role_id': 1, '_secret': 'x', 'password': 'x', 'id': 1}
```
Serialize the instance of the User model into the three-dimensional dictionary and exclude a few attributes using different methods:
```python

>>> row2dict(user, depth=3, exclude_pk=True, exclude_underscore=True)
{'username': 'yarbshk', 'password': 'x', 'id': 1, 'role': {'description': None, 'id': 1, 'permissions': [{'id': 1, 'name': 'posts:r'}, {'id': 2, 'name': 'posts:w'}], 'name': 'Moderator'}}
>>> row2dict(user, depth=3, exclude={'role_id', '_secret'})
{'username': 'yarbshk', 'password': 'x', 'id': 1, 'role': {'description': None, 'id': 1, 'permissions': [{'id': 1, 'name': 'posts:r'}, {'id': 2, 'name': 'posts:w'}], 'name': 'Moderator'}}

```
Serialize the instance of the User model and store one in a local variable to work with:
```python
>>> user_dict = row2dict(user, depth=3)
>>> user_dict
{'username': 'yarbshk', 'role': {'description': None, 'id': 1, 'permissions': [{'id': 1, 'name': 'posts:r'}, {'id': 2, 'name': 'posts:w'}], 'name': 'Moderator'}, 'role_id': 1, '_secret': 'x', 'password': 'x', 'id': 1}
```

Suppose in other part of the application you need to **deserialize that dictionary** to be able to use all features of the User's model (e.g. calling methods, querying data):
```python
>>> dict2row(user_dict, User)
<User (transient 139927902911456)>
```
The example above will create new instance of the User model without any relations (such as _role_ or _permissions_). To create a user's instance with all relations it's necessary to explicitly specify the models (Role, Permission) for that relations:
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

Arguments of the `dict2row()` method which left unnoticed (_exclude_, _exclude_pk_, _exclude_underscore_) works as same as in the `row2dict()` method.

## Pay attention

If you want to exclude some attribute of model which has synonym (and vice versa) you MUST exclude both attribute and synonym (in other case SQLAlchemy automatically sets the same value for attribute and their synonym even if one of them is excluded):

```python
>>> dict2row(user_dict, User, exclude={'attr', 'synonym'})
```

## Documentation

> Note that **default values** of the optional arguments in methods below **are setting implicitly**. This behavior is required by class DictionarySerializableModel (see detailed explanation below).

### row2dict(row, depth=None, exclude=None, exclude_pk=None, exclude_underscore=None, only=None, fk_suffix=None)

Recursively walk row attributes to serialize ones into a dict.

- **row** (required) – _instance_ of the declarative base class (base SQLAlchemy model).
- **depth** (optional, default: `1`) – _number_ that represent the depth of related relationships.
- **exclude** (optional, default: `set()`) – _set_ of attributes names to exclude.
- **exclude_pk** (optional, default: `False`) – _are_ foreign keys (e.g. fk_name_id) excluded.
- **exclude_underscore** (optional, default: `False`) – _are_ private and protected attributes excluded.
- **only** (optional, default: `set()`) – _set_ of attributes names to include.
- **fk_suffix** (optional, default: `_id`) – _str_ that represent a foreign key suffix.

### dict2row(d, model, rel=None, exclude=None, exclude_pk=None, exclude_underscore=None, only=None, fk_suffix=None)

Recursively walk dict attributes to serialize ones into a row.

- **d** (required) – _dict_ which represent a serialized row.
- **model** (required) – _class_ nested from the declarative base class.
- **rel** (optional, default: `{}`) – _dict_ of key (relationship name) -value (class) pairs.
- **exclude** (optional, default: `set()`) – _set_ of attributes names to exclude.
- **exclude_pk** (optional, default: `False`) – _are_ foreign keys (e.g. fk_name_id) excluded.
- **exclude_underscore** (optional, default: `False`) – _are_ private and protected attributes excluded.
- **only** (optional, default: `set()`) – _set_ of attributes names to include.
- **fk_suffix** (optional, default: `_id`) – _str_ that represent a foreign key suffix.

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
    ...
    _sa_dst_exclude_pk = True
    _sa_dst_exclude_underscore = True
    ...
```

The class declaration above is equal to calling the following method:

```python
>>> user.as_dict(exclude_pk=True, exclude_underscore=True)
{'username': 'yarbshk', 'id': 1, 'password': 'x', 'role': None}
``` 

We're calling the method below without parameters, because configuration attributes with prefix `_sa_dst_` are set in the model above:

```python
>>> user.as_dict() # analog of row2dict(user, exclude_pk=True, exclude_underscore=True)
{'username': 'yarbshk', 'id': 1, 'password': 'x', 'role': None}
```

The following **configuration attributes** are available in models:
* **_sa_dst_depth**
* **_sa_dst_exclude**
* **_sa_dst_exclude_pk**
* **_sa_dst_exclude_underscore**
* **_sa_dst_only**
* **_sa_dst_rel**
* **_sa_dst_fk_suffix**

You can see an example of instantiating Flask + SQLAlchemy with `DictionarySerializableModel` in the `tests/main.py` file. 

## Copyright and License
Copyright (c) 2018 Yuriy Rabeshko. Code released under the MIT license.
