from flask import Flask

import settings
from apps.viwes.view import bp

from exts import db


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings)
    print(app.config)
    # 添加数据库扩展
    db.init_app(app)
    # 注册蓝图
    app.register_blueprint(bp)
    print(app.url_map)

    return app
