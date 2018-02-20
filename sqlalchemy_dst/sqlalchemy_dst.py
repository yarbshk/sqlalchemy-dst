from sqlalchemy.orm import collections


ATTR_DEPTH = '_sa_dst_depth'
ATTR_EXCLUDE = '_sa_dst_exclude'
ATTR_EXCLUDE_PK = '_sa_dst_exclude_pk'
ATTR_EXCLUDE_UNDERSCORE = '_sa_dst_exclude_underscore'
ATTR_ONLY = '_sa_dst_only'
ATTR_REL = '_sa_dst_rel'
ATTR_FK_SUFFIX = '_sa_dst_fk_suffix'

DEFAULT_DEPTH = 1
DEFAULT_EXCLUDE = set()
DEFAULT_EXCLUDE_PK = False
DEFAULT_EXCLUDE_UNDERSCORE = False
DEFAULT_ONLY = set()
DEFAULT_REL = dict()
DEFAULT_FK_SUFFIX = '_id'


def get_mapper(row):
    """
    Tries to get the mapper from a row instance.
    http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping

    :param row: instance of the declarative base class

    :return: instance of :class:`sqlalchemy.orm.mapper.Mapper`
    """
    try:
        mapper = getattr(row, '__mapper__')
    except AttributeError as e:
        e.args = ('Row must be instance of the declarative base class, '
                  'got %s instead' % type(row).__name__,)
        raise

    return mapper

def get_backref(rel):
    backref = rel.backref or rel.back_populates
    if backref:
        return str(backref)

def get_fk_suffix(row):
    return getattr(row, ATTR_EXCLUDE_PK, DEFAULT_EXCLUDE_PK)

check_only = lambda x, only: len(only) and x not in only
check_exclude_pk = lambda x, exclude_pk, fk_suffix='': \
    x.endswith(fk_suffix) and exclude_pk
check_exclude_underscore = lambda x, exclude_underscore: \
    x.startswith('_') and exclude_underscore

def row2dict(row, depth=None, exclude=None, exclude_pk=None,
             exclude_underscore=None, only=None, fk_suffix=None):
    """
    Recursively walk row attributes to serialize ones into a dict.

    :param row: instance of the declarative base class
    :param depth: number that represent the depth of related relationships
    :param exclude: set of attributes names to exclude
    :param exclude_pk: are foreign keys (e.g. fk_name_id) excluded
    :param exclude_underscore: are private and protected attributes excluded
    :param only: set of attributes names to include
    :param fk_suffix: str that represent a foreign key suffix

    :return: dict with attributes of current depth level
    """
    if depth == 0:
        return None
    d, mapper = {}, get_mapper(row)
    if depth is None:
        depth = getattr(row, ATTR_DEPTH, DEFAULT_DEPTH) - 1
    else:
        depth -= 1
    if exclude is None:
        exclude = getattr(row, ATTR_EXCLUDE, DEFAULT_EXCLUDE)
    if exclude_pk is None:
        exclude_pk = getattr(row, ATTR_EXCLUDE_PK, DEFAULT_EXCLUDE_PK)
    if exclude_underscore is None:
        exclude_underscore = getattr(row, ATTR_EXCLUDE_UNDERSCORE,
                                     DEFAULT_EXCLUDE_UNDERSCORE)
    if only is None:
        only = getattr(row, ATTR_ONLY, DEFAULT_ONLY)
    if fk_suffix is None:
        fk_suffix = getattr(row, ATTR_FK_SUFFIX, DEFAULT_FK_SUFFIX)
    for c in mapper.columns.keys() + mapper.synonyms.keys():
        if c in exclude or \
                check_exclude_pk(c, exclude_pk, fk_suffix=fk_suffix) or \
                check_exclude_underscore(c, exclude_underscore) or \
                check_only(c, only):
            continue
        d[c] = getattr(row, c)
    for r in mapper.relationships.keys():
        if r in exclude or check_only(r, only):
            continue
        attr = getattr(row, r)
        backref = get_backref(mapper.relationships[r])
        if backref:
            exclude.add(backref)
        kwargs = dict(depth=depth, exclude=exclude, exclude_pk=exclude_pk,
                      exclude_underscore=exclude_underscore, only=only,
                      fk_suffix=fk_suffix)
        if isinstance(attr, collections.InstrumentedList):
            d[r] = [row2dict(i, **kwargs) for i in attr if depth]
        else:
            d[r] = row2dict(attr, **kwargs)

    return d

def dict2row(d, model, rel=None, exclude=None, exclude_pk=None,
             exclude_underscore=None, only=None, fk_suffix=None):
    """
    Recursively walk dict attributes to serialize ones into a row.

    :param d: dict that represent a serialized row
    :param model: class nested from the declarative base class
    :param rel: dict of key (relationship name) -value (class) pairs
    :param exclude: set of attributes names to exclude
    :param exclude_pk: are foreign keys (e.g. fk_name_id) excluded
    :param exclude_underscore: are private and protected attributes excluded
    :param only: set of attributes names to include
    :param fk_suffix: str that represent a foreign key suffix

    :return: instance of the declarative base class
    """
    if not isinstance(d, dict):
        raise TypeError('Source must be instance of dict, got %s instead' %
                        type(d).__name__)
    row = model()
    mapper = get_mapper(row)
    if rel is None:
        rel = getattr(row, ATTR_REL, DEFAULT_REL)
    if exclude is None:
        exclude = getattr(row, ATTR_EXCLUDE, DEFAULT_EXCLUDE)
    if exclude_pk is None:
        exclude_pk = getattr(row, ATTR_EXCLUDE_PK, DEFAULT_EXCLUDE_PK)
    if exclude_underscore is None:
        exclude_underscore = getattr(row, ATTR_EXCLUDE_UNDERSCORE,
                                     DEFAULT_EXCLUDE_UNDERSCORE)
    if only is None:
        only = getattr(row, ATTR_ONLY, DEFAULT_ONLY)
    if fk_suffix is None:
        fk_suffix = getattr(row, ATTR_FK_SUFFIX, DEFAULT_FK_SUFFIX)
    for c in mapper.columns.keys() + mapper.synonyms.keys():
        if c not in d or c in exclude or \
                check_exclude_pk(c, exclude_pk, fk_suffix=fk_suffix) or \
                check_exclude_underscore(c, exclude_underscore) or \
                check_only(c, only):
            continue
        setattr(row, c, d[c])
    for r in mapper.relationships.keys():
        if r not in d or r not in rel or check_only(r, only):
            continue
        kwargs = dict(rel=rel, exclude=exclude, exclude_pk=exclude_pk,
                      exclude_underscore=exclude_underscore, only=only,
                      fk_suffix=fk_suffix)
        if isinstance(d[r], list):
            setattr(row, r, collections.InstrumentedList())
            for i in d[r]:
                getattr(row, r).append(dict2row(i, rel[r], **kwargs))
        else:
            if not exclude_pk:
                rpk = d[r].get('id') if isinstance(d[r], dict) else None
                setattr(row, r + fk_suffix, rpk)
            setattr(row, r, dict2row(d[r], rel[r], **kwargs))

    return row


class DictionarySerializableModel:
    def as_dict(self, **kwargs):
        return row2dict(self, **kwargs)

    @classmethod
    def from_dict(cls, d, **kwargs):
        return dict2row(d, cls, **kwargs)

    def __iter__(self):
        for i in self.as_dict().items():
            yield i
