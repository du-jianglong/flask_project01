# 脚本文件
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
# 导入数据表模型
from models import User, Question, Comment

manager = Manager(app)

# 使用　Migrate 绑定　app 和　db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到　manager　中
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
