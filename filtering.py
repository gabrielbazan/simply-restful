
class Filter(object):

    map = {
        'gt': '>', 'gte': '>=',
        'lt': '<', 'lte': '<=',

        'intersects': '',

        'in': 'in_', 'notin': 'notin_',
        'like': 'like', 'notlike': 'notlike',
        'ilike': 'ilike', 'notilike': 'notilike',
        'is': 'is_', 'isnot': 'isnot'
    }

    def __init__(self, model, filters):
        self.model = model
        self.filters = filters

    def to_orm(self):
        import sqlalchemy
        from sqlalchemy import and_
        orm = []
        print 'self.filters: ', self.filters
        for f, v in self.filters.iteritems():
            split = f.split('__')
            column, operation = split if len(split) == 2 else f, 'is'

            print 'column, operation: ', column, operation
            print 'column: ', column
            print 'value: ', v
            orm.append(
                getattr(
                    getattr(self.model, column),
                    self.map[operation]
                )(v)
            )

        return and_(*orm)

    """
        q.filter(
            Filter(self.model, filters).to_orm()
        )
    """
