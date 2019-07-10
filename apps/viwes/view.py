import os
from datetime import timedelta

from flask import Blueprint, render_template, request, make_response, redirect, url_for, session, g, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash

from apps.models.model import User, Book, Cart
from exts import db
from settings import UPLOAD_DIR

bp = Blueprint('shop', __name__)

login_list = ['/addcart', '/showcart']


@bp.before_app_request
def process_request():
    if request.path in login_list:
        username = session.get('username')
        print(username)
        if not username:
            # 判断是否是ajax请求
            if request.is_xhr:
                # 返回jsonify
                return jsonify({'status': 403})
            else:
                return render_template('login.html')
        else:
            print('---->3')
            g.username = username


@bp.after_app_request
def process_response(response):
    print(response.headers)
    print('**************>>>>>')
    return response


@bp.before_app_first_request
def first_request():
    print('------------->first')


@bp.app_errorhandler(404)
def file_notfound(error):
    return render_template('404.html')


@bp.app_errorhandler(500)
def internal_error(error):
    print(error)
    return render_template('500.html')


@bp.route('/')
def index():
    # username = request.cookies.get('username')   从cookies中取值
    username = session.get('username')  # 获取session中的username
    # 查询图书
    # books = Book.query.all()
    # abort(500)  # rasie 一个HttpException
    # 获取页码数
    page = request.args.get('page', 1)
    pagination = Book.query.paginate(page=int(page), per_page=3)

    return render_template('index.html', username=username, pagination=pagination)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username', None)
        print(username)
        password = request.form.get('password', None)
        print(password)  # ''  None
        repassword = request.form.get('repassword')

        if username and password and repassword:

            if password == repassword:
                user = User.query.filter(User.username == username).first()
                # user = User.query.filter_by(username=username).first()
                if not user:
                    # 注册
                    user = User()
                    user.username = username
                    hash_password = generate_password_hash(password)
                    user.password = hash_password

                    # db.session.add(user)
                    # db.session.commit()
                    flag = user.save()
                    if flag:
                        return '用户注册成功'


                else:
                    # 用户已经注册
                    return render_template('register.html', msg='此用户名已被占用')
            else:
                # 密码不一致
                return render_template('register.html', msg='密码不一致')
        else:
            return render_template('register.html', msg='必须输入用户名或者密码')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if username and password:

            user = User.query.filter(User.username == username).first()
            if user:
                result = check_password_hash(user.password, password)
                if result:
                    # 用户登录成功  cookie保存
                    # response = make_response('登录成功！')
                    # response.headers['Content-Type'] = 'text/html;charset=utf-8'
                    # response.set_cookie('username', username)
                    # return response

                    # 服务器保存 session 当成字典
                    session['username'] = username
                    return redirect(url_for('shop.index'))


                else:
                    render_template('login.html', msg='用户名或者密码错误')
            else:
                return render_template('login.html', msg='没有此用户')

        else:
            return render_template('login.html', msg='必须输入用户名或者密码')


@bp.route('/logout')
def logout():
    # response = redirect(url_for('shop.index'))
    # response.delete_cookie('username')  # 相当于把客户端浏览器中的cookie删除
    # return response

    # session中的清空
    # del session['username']
    session.clear()
    return redirect(url_for('shop.index'))


# 添加购物车
@bp.route('/addcart')
def addCart():
    user = User.query.filter(User.username == g.username).first()
    bookid = request.args.get('bookid')
    data = {}
    try:
        cart1 = Cart.query.filter(Cart.bookid == bookid, Cart.userid == user.id).first()
        if not cart1:
            # 添加到购物车中
            cart = Cart()
            cart.userid = user.id
            cart.bookid = bookid

            db.session.add(cart)

        else:
            cart1.numbers += 1
        db.session.commit()
        data['status'] = 201

    except:
        data['status'] = 500

    return jsonify(data)


# 查看购物车
@bp.route('/showcart')
def showCart():
    user = User.query.filter(User.username == g.username).first()
    carts = Cart.query.filter(Cart.userid == user.id).all()
    print('=================>>>>>>')
    return render_template('show.html', user=user, carts=carts)


@bp.route('/search', methods=['GET', 'POST'])
def search():
    content = request.form.get('content')

    books = Book.query.filter(Book.title.contains(content)).all()

    return render_template('search.html', books=books)


@bp.route('/center/<name>', methods=['GET', 'POST'])
def center(name):
    user = User.query.filter(User.username == name).first()
    if request.method == 'GET':

        return render_template('center.html', user=user)
    else:
        # 获取表单的数据
        # phone = request.form.get('phone')
        storage = request.files.get('icon')  # 文件存储对象
        print(storage.filename)
        user.icon = 'upload/'+storage.filename
        user.save()
        # 文件的本地保存
        file_path = os.path.join(UPLOAD_DIR,storage.filename)
        # with open(file_path,'wb') as fw:
        #     fw.write(storage.read())
        storage.save(file_path)


        return render_template('center.html', user=user)
