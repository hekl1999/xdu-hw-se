import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 基类
class Config:
    SECRET_KEY = 'one more seconds'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flask]'
    FLASKY_MAIL_SENDER = 'Flask Admin'
    FLASKY_ADMIN = ['16130120129'] #  super admin
    UPLOADED_PHOTOS_DEST  = os.path.join(basedir,'photos')

    @staticmethod
    def init_app(app):
        pass

# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')  # 我本机的测试数据库,暂时使用sqlite

# 测试环境
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxxxx@xxx.xxx.xxx.xxx:3306/data_test'

# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:xxxxxx@127.0.0.1:3306/production'

# 设置一个config 字典中,注册了不同的配置环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
