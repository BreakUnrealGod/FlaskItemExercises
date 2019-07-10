from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps.models.model import User,Book,Cart
from apps import create_app
from exts import db


app = create_app()

manager = Manager(app=app)

# 添加命令
migrate = Migrate(app=app, db=db)  # 整合app和db对象

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
