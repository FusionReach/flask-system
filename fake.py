from app import create_app
from app.models.base import db
from app.models.user import User

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        with db.auto_commit():
            # 创建一个管理员
            user = User()
            user.username = user.nickname = 'admin'
            user.password = 'admin'
            user.permission = 1
            user.status = 1
            db.session.add(user)

            # 创建一个普通用户
            user = User()
            user.username = user.nickname = 'test'
            user.password = 'test'
            user.permission = 0
            user.status = 1
            db.session.add(user)
