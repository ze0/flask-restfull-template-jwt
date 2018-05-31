class Configuration(object):
    VERSION = '1.0.0'
    DEBUG = True
    STATUS = 'UNKNOW'

    SECRET_KEY = '1b19215464db2b0eb2a74531f8254c3dfac175794b928674016dda1fb024265f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = '0.0.0.0'
    PORT = 5000


class Development(Configuration):
    STATUS = 'DEVELOPMENT'