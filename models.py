from exts import db
from datetime import datetime

'''
比如说，将 user　模型映射到数据库中：
    1、在　models.py 中建好数据表模型，并在　manage.py 中导入模型

    2、在根目录下：python manage.py db init    （初始化数据库迁移环境，只在项目第一次使用时执行）
    
    3、执行：python manage.py db migrate   (将模型映射到数据库中，此刻数据库中增加数据库版本，模型还未真正映射成功) => 数据库升级
        这里遇到第二行命令报错：
            ＃return __import__('MySQLdb')
            ＃ModuleNotFoundError: No module named 'MySQLdb'
            
        这是没有安装　MySQLdb　执行：　pip install MySQLdb
        
        再次执行，继续报错：
            ＃self.encoding = charset_by_name(self.charset).encoding
            ＃AttributeError: 'NoneType' object has no attribute 'encoding'
            
        这里使用　pymysql　，使用　mysqldb　将会报错
        注意编码问题：utf8
        DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
        
    4、将模型真正映射到数据库中：python manage.py db upgrade
'''


# 用户表模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(11), nullable=False)
    nickname = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(100), nullable=False)


# 问答模型
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取服务器第一次运行时间，之后每次创建新数据模型时间都是一样的，时间不会更新
    # now　每次创建新数据模型都会调　now　这个函数，时间会更新
    create_time = db.Column(db.DateTime, default=datetime.now)
    # ForeignKey 指定外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # backref 反转： 通过 question 查找　user 发布的所有问答
    author = db.relationship('User', backref=db.backref('question'))


# 评论模型
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question', backref=db.backref('comment', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('comment'))
