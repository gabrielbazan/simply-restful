from resource import Resource


def add_resource(api, resource, identifier_type='int'):
    endpoint = resource.endpoint

    api.add_resource(
        resource,
        '/{}'.format(endpoint),
        methods=['GET', 'POST'],
        endpoint='{}-list'.format(endpoint)
    )

    api.add_resource(
        resource,
        '/{}/<{}:id>'.format(endpoint, identifier_type),
        methods=['GET', 'PUT', 'DELETE'],
        endpoint=endpoint + '-detail'
    )
