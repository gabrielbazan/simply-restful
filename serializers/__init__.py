from database import session
from settings import DATE_FORMAT
from datetime import datetime
from settings import DEFAULT_AUTHENTICATION, DEFAULT_AUTHORIZATION

from models import get_class_by_table_name
from filtering import Filter


class Serializer(object):
    authenticators = []
    authorizers = []
    validators = []
    fields = None

    methods = {
        datetime: lambda x: x.strftime(DATE_FORMAT)
    }

    @property
    def model(self):
        raise NotImplementedError

    def __init__(self):
        self.query = session.query(self.model)
        if not self.authenticators:
            self.authenticators = [
                instantiate(a) for a in DEFAULT_AUTHENTICATION
            ]
        if not self.authorizers:
            self.authorizers = [
                instantiate(a) for a in DEFAULT_AUTHORIZATION
            ]
        self.user = self._authenticate()

    def create(self, data):
        instance = self.model()
        self.deserialize(data, instance)
        session.add(instance)
        session.flush()
        serial = self.serialize(instance)
        session.commit()
        return serial

    def update(self, id, data):
        instance = self.query.get(id)
        self.deserialize(data, instance)
        session.flush()
        serial = self.serialize(instance)
        session.commit()
        return serial

    def read(self, id):
        return self.serialize(self.query.get(id))

    def list(self, filters):
        columns = [c.name for c in self.model.__table__.columns]
        # filters = {k: v for k, v in filters.iteritems() if k in columns}

        cond = Filter(self.model, filters).to_orm()
        print 'cond: ', cond

        return dict(
            # self.query.filter_by(**filters).all()
            results=[self.serialize(m) for m in self.query.filter(cond).all()],
            count=self.query.count()
        )

    def delete(self, id):
        return self.query.filter_by(id=id).delete()

    def serialize(self, instance):
        serialized = dict()
        for prop in instance.__table__.columns:
            name = prop.name
            if not self.fields or name in self.fields:
                value = getattr(instance, name)
                value_type = type(value)

                if value_type in self.methods:
                    value = self.methods[value_type](value)

                relationships = instance.relationships
                if name in relationships and getattr(self, relationships[name], None):
                    value = getattr(self, relationships[name])().serialize(
                        getattr(instance, relationships[name])
                    )

                serialized[name] = value
        return serialized

    def deserialize(self, data, instance):
        for relationship in instance.__mapper__.relationships:
            target = relationship.local_remote_pairs[0][1]
            key = relationship.key
            if data.get(key):
                fields = data.get(key)
                target_class = get_class_by_table_name(target.table.name)
                value = session.query(target_class).filter_by(**fields).first()
                data[key] = value

        for prop in data:
            if prop not in instance.primary_keys:
                setattr(instance, prop, data.get(prop))

    def _authenticate(self):
        for authenticator in self.authenticators:
            user = authenticator.authenticate()
            if user:
                return user
        raise Exception('Authentication error')

    def _authorize(self):
        for authorizer in self.authorizers:
            authorizer.authorize()

    def _validate(self):
        for validator in self.validators:
            validator.validate()


def instantiate(class_string):
    from importlib import import_module
    module_name, class_name = class_string.rsplit('.', 1)
    try:
        module_ = import_module(module_name)
        try:
            class_ = getattr(module_, class_name)()
        except AttributeError:
            raise Exception('Class does not exist')
    except ImportError:
        raise Exception('Module does not exist')
    return class_ or None
