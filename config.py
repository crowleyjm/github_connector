import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = "postgres://ovsoaajreppuyb:84014559fb7014e2af3c263d4e30f1afb37196a7d511cd882df4a8302ba1891d@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dfq49p3g24hncm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
