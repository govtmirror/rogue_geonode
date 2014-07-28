__version__ = (0, 1, 0, 'alpha', 0)


def get_version():
    import geonode.version
    return geonode.version.get_version(__version__)
