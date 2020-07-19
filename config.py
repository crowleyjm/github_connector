import os

LOCAL_DEBUG = False

class Config(object):
    POSTS_PER_PAGE = 10
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    DATABASE_URL = None
    if LOCAL_DEBUG:
        DATABASE_URL="postgres://test_user:N2JdjiKyfp@127.0.0.1/github_connector"
    else:
        DATABASE_URL = "postgres://ovsoaajreppuyb:84014559fb7014e2af3c263d4e30f1afb37196a7d511cd882df4a8302ba1891d@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dfq49p3g24hncm"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False