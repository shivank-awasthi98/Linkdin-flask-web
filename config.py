import os
class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or b'!\x8a\x98jF\xa5\xeb\xb4\xc8z\xba\xe6\x89\x86\xbfk'




    MONGODB_SETTINGS = {'db':'UTA_Enrollment',
        'host': 'mongodb://localhost:27017/UTA_Enrollment'
    }