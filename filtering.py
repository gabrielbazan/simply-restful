from sqlalchemy import and_


class Filter(object):

    map = {
        'eq': '__eq__',
        'gt': '__gt__', 'ge': '__ge__',
        'lt': '__lt__', 'le': '__le__',
        'in': 'in_', 'notin': 'notin_',
        'like': 'like', 'notlike': 'notlike',
        'ilike': 'ilike', 'notilike': 'notilike',
        'is': 'is_', 'isnot': 'isnot',
        'intersects': ''
    }

    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

    @property
    def join(self):
        a = self.model().relationship_classes
        print a
        return a

    @property
    def filter(self):
        orm = []
        for f, value in self.filters.iteritems():
            split = f.split('__')

            last = split[-1]

            op = split.pop() if last in self.map else 'eq'

            # self.model.province.property.mapper.class_

            column = self.model.province.property.mapper.class_.id

            #model = self.model
            #for c in split:
            #    column = getattr(model, c)

            print 'column, operation, value: ', column, op, value

            orm.append(
                getattr(column, self.map[op])(value)
            )

        return and_(*orm)
