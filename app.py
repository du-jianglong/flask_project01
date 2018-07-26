from flask import Flask, render_template, request, redirect, url_for, session, flash
import config
from exts import db
from models import User, Question, Comment
from decorators import login_required

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)  # 初始化 db


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


# 登录视图函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        # 验证该手机和是否有注册
        user = User.query.filter(User.mobile == mobile, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内免登录,或者是自定义天数请在　config.py　中设置　PERMANENT_SESSION_LIFETIME
            if remember_me == 'on':
                session.permanent = True
            return redirect(url_for('index'))
        elif mobile == '':
            flash('请输入手机号！')
        elif password == '':
            flash('请输入密码！')
        else:
            flash('用户名或密码有误，请重新输入！')
        return render_template('login.html')


# 注册视图函数
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        mobile = request.form.get('mobile')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')

        # 手机好验证，如已注册，将不能再次注册
        user = User.query.filter(User.mobile == mobile).first()
        if user:
            return '该手机号已被注册过了，换个手机号试试吧！'
        else:
            # 验证密码和确认密码是否一致
            if password == '' or repeat_password == '':
                return '密码不能为空值！'
            elif password != repeat_password:
                return '两次密码输入不一样！'
            else:
                user = User(mobile=mobile, nickname=nickname, password=password)
                db.session.add(user)
                db.session.commit()
                # 注册成功，跳转至登录页
                return redirect(url_for('login'))


# 上下文处理器——登录状态
# 返回的字典在所有的页面中都是可用的
# 被这个装饰器修饰的钩子函数，必须返回一个字典，即使为空值
@app.context_processor
def my_context_process():
    # 通过 session['user_id'] 如果没有，将抛出异常
    # 使用　session.get('user_id')　会返回（具体值／None）
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    else:
        return {}


# 注销登录
@app.route('/logout/')
def logout():
    # 删除　session 有以下3种方式
    # session.pop('user_id')
    # del session['user_id']
    # session.clear()   # 清除所有 session 记录
    session.pop('user_id')
    return redirect(url_for('login'))


# 发布问答
@app.route('/requestion/', methods=['GET', 'POST'])
@login_required
def requestion():
    if request.method == 'GET':
        return render_template('requestion.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


'''
传值的时候需注意：
route　和函数　 中需要填入相应的参数名
模板中，例如：<a href="{{ url_for('details', question_id=question.id) }}">跳转</a>
三者缺一不可
'''


# 详情试图函数
@app.route('/details/<question_id>/')
def details(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    # 获取评论数量
    comment_len = len(question_model.comment)
    # 将获取到的内容直接传入木板中，如下：
    return render_template('details.html', question_model=question_model, comment_len=comment_len)


# 评论试图函数
@app.route('/details_comment/', methods=['POST'])
@login_required
def details_comment():
    content = request.form.get('content')
    comment = Comment(content=content)
    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('details', question_id=question_id))


if __name__ == '__main__':
    app.run()
