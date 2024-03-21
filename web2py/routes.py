routes_in = (
    ('/', '/urk/static/index.html'),
    ('/urk/default/(?P<any>.*)', '/urk/default/\g<any>'),
    ('/(?P<any>.+\..+)$', '/urk/static/\g<any>'),
    ('/(?P<any>[^/]+(/[^/]+)*)$', '/urk/static/\g<any>.html'),
    ('/(?P<any>[^/]+(/[^/]+)*)/$', '/urk/static/\g<any>/index.html'),
)
