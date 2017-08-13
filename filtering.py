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
        'intersects': 'ST_Intersects',
        'contains': 'ST_Intersects'
    }

    multiple = ['in', 'notin']  # Between

    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

    def translate(self):
        orm = []
        joins = []
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

        return and_(*orm), joins


"""
{
    'id': 1,                                [id]                                [id, eq]
    'id__gt': 1,                            [id]                                [id, gt]
    'province__id': 1,                      [province, id]                      [province, id, eq]
    'province__id__ge': 1,                  [province, id, ge]                  [province, id, ge]
    'province__state__name: 'LA',           [province, state, name]             [province, state, name, eq]
    'province__state__population__gt': 1    [province, state, population, gt]   [province, state, population, gt]
}
"""
