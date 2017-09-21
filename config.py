class ProductionConfig():
	DEBUG = False
	TESTING = False
	MONGO_DBNAME = 'demo'
	MONGO_URI = 'mongodb://localhost:27017/' + MONGO_DBNAME

class DevelopmentConfig():
    DEBUG = True
    TESTING = False
    MONGO_DBNAME = 'demo'
    MONGO_URI = 'mongodb://localhost:27017/' + MONGO_DBNAME
    LOGS_URI = 'http://localhost:5000/logs/'
    NOTIFY_ERRORS = {'-9', 'error',
                     '-7', 'warning',
                     '-100', 'info'}
    MAILER_DEST = {'error': ['cristi.domsa@gmail.com'],
                   'warning': ['cristi.domsa@gmail.com'],
                   'info': ['cristi.domsa@gmail.com']}

    ASSETS_PATH = './assets/'
    UPLOAD_PATH = './assets/uploads/'
    ALLOWED_EXTENSIONS = set(['png'])

class TestingConfig():
    DEBUG = False
    TESTING = True
    MONGO_DBNAME = 'demo'
    MONGO_URI = 'mongodb://localhost:27017/' + MONGO_DBNAME