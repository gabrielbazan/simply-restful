from sqlalchemy import and_
from settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class Filter(object):

    map = {
        'eq': '__eq__',
        'gt': '__gt__', 'ge': '__ge__',
        'lt': '__lt__', 'le': '__le__',
        'in': 'in_', 'notin': 'notin_',
        'like': 'like', 'notlike': 'notlike',
        'ilike': 'ilike', 'notilike': 'notilike',
        'is': 'is_', 'isnot': 'isnot',
        'intersects': 'ST_Intersects',
        'contains': 'ST_Intersects'
    }

    multiple = ['in', 'notin']  # TODO: Implement Between filter

    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

    def translate(self):
        orm = []
        joins = []

        size = int(self.filters.pop('limit', DEFAULT_PAGE_SIZE))
        limit = MAX_PAGE_SIZE if size > MAX_PAGE_SIZE else size
        offset = int(self.filters.pop('offset', 0))

        order = self.filters.pop('order_by', None)
        print order

        for f, value in self.filters.iteritems():
            split = f.split('__')

            last = split[-1]

            op = split.pop() if last in self.map else 'eq'

            column_name = split.pop()

            model = self.model
            for nested in split:
                model = getattr(model, nested).mapper.class_
                joins.append(model)

            if op in self.multiple:
                value = value.split(';')

            orm.append(
                getattr(
                    getattr(model, column_name),
                    self.map[op]
                )(value)
            )

        return and_(*orm), joins, limit, offset
