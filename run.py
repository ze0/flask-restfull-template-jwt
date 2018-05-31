from API import create_app
from API.configuration import Development


app = create_app(Development)

if app.config['STATUS'] == 'PRODUCTION':
    context = ('cert/cert.pem', 'cert/key.pem')
    app.run(host=app.config['HOST'], port=app.config['PORT'], ssl_context=context)
else:
    app.run(host=app.config['HOST'], port=app.config['PORT'])
