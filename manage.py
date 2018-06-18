# encoding:utf-8

from flask_script import Manager
from app import app
from exts import db
from flask_migrate import Migrate, MigrateCommand
import models


manager = Manager(app)

migrate = Migrate(app, db)


'''
通过 python manage.py db init     初始化
通过 python manage.py db migrate  生成当前版本
通过 python manage.py db upgrade  更新版本
'''
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    print('Manager可以使用！')


if __name__ == '__main__':
    manager.run()
