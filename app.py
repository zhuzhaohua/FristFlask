# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
import config
from exts import db, main_url, html_unescape
from models import Note, Tag, User, Message
import os
import datetime
from decorators import login_required


app = Flask(__name__)
# 在APP中加载配置
app.config.from_object(config)
db.init_app(app)


# 原始路由 主页入口
@app.route('/')
def index():
    notes = Note.query.order_by('-create_time').all()
    return render_template('index.html', notes=notes)


# 笔记录入的视图函数
@app.route('/note/', methods=['GET', 'POST'])
@login_required
def note():
    if request.method == 'GET':
        return render_template('note.html')
    else:
        title = request.form.get('note-title')
        tag_content = request.form.get('note-tag')
        tags = tag_content.split(',')
        content = request.form.get('note-content')
        note = Note(title=title, content=content)

        for tag_text in tags:
            tag = Tag(tag=tag_text, text=tag_text)
            note.tags.append(tag)

        db.session.merge(note)
        db.session.commit()

        return redirect(url_for('index'))


# 详情画面
@app.route('/detail/<note_id>/')
def detail(note_id):
    note = Note.query.filter(Note.id == note_id).first()
    return render_template('detail.html', note=note, count=len(note.messages))


# 编辑的视图函数
@app.route('/settingEdit/')
@login_required
def setting_edit():
    notes = Note.query.order_by('-create_time').all()
    return render_template('setting.html', notes=notes)


# 详情以及回答的视图函数
@app.route('/edit/<note_id>/', methods=['GET', 'POST'])
@login_required
def edit(note_id):
    note = Note.query.filter(Note.id == note_id).first()

    tags_out = ''
    for tag in note.tags:
        tags_out = tags_out + tag.tag + ","

    txt = html_unescape(note.content)

    note_new = {'title': note.title, 'tags': tags_out, 'content': txt}
    if request.method == 'GET':
        return render_template('edit.html', note=note_new)
    else:
        title = request.form.get('note-title')
        tag_content = request.form.get('note-tag')
        tags = tag_content.split(',')
        content = request.form.get('note-content')
        note.title = title
        note.content = content

        note.tags = []
        for tag_text in tags:

            tag_tmp = Tag.query.filter(Tag.tag == tag_text).first()

            if tag_tmp:
                note.tags.append(tag_tmp)
            else:
                tag = Tag(tag=tag_text, text=tag_text)
                note.tags.append(tag)

        db.session.commit()

        return redirect(url_for('index'))


# 图片上传的视图函数
@app.route('/upload/', methods=['POST'])
@login_required
def upload_img():
    file_obj = request.files.get('picture')
    date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = os.path.join('static/images', date_str + '_' + file_obj.filename)
    with open(file_path, 'wb') as f:
        f.write(file_obj.read())

    file_obj.close()
    return main_url + file_path


# 标签分组
@app.route('/query/<condition>')
def query_tag(condition):
    if request.method == 'GET':
        tag = Tag.query.filter(Tag.tag == condition).first()
        notes = tag.notes

        return render_template('query.html', notes=notes, condition=condition + u' 标签的笔记如下：')


# 查询功能
@app.route('/query/', methods=['POST'])
def query_condition():
    condition_text = request.form.get('conditionText')

    notes = Note.query.filter(Note.content.like("%" + condition_text + "%")).all()
    return render_template('query.html', notes=notes, condition=condition_text + u' 的查询结果如下：')


# 登录视图函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        email = request.args.get('email')
        if email:
            return render_template('login.html', email=email)
        else:
            return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        me = request.form.get('me')
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果30天内不想重复登录
            if me:
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return '账号或密码错误，请重新登录或注册'


# 注册的试图函数
@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        phoneno = request.form.get('phoneNo')
        username = request.form.get('userName')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 手机号码验证
        user = User.query.filter(User.email == email).first()

        if user:
            return '该邮箱已经被注册 请登录或修改邮箱'
        else:
            if password != password2:
                return '两次密码不一致，请确认'
            else:
                user = User(email=email, phoneno=phoneno, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login', email=email))


# 注销的视图函数
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    # 注销后 回到登录画面
    return redirect(url_for('login'))


@app.route('/message/', methods=['POST'])
@login_required
def message():
    user_id = session.get('user_id')
    content = request.form.get('messageContent')
    note_id = request.form.get('note_id')
    message = Message(content=content, note_id=note_id, user_id=user_id)
    message.user = User.query.filter(User.id == user_id).first()
    message.note = Note.query.filter(Note.id == note_id).first()

    db.session.add(message)
    db.session.commit()

    return redirect(url_for('detail', note_id=note_id))


# 钩子函数 上下文 在每次请求时，获取所有标签
@app.context_processor
def my_context_processor():
    tags = Tag.query.all()
    user_id = session.get('user_id')

    ret = dict()

    if tags:
        tags = set([tag.tag for tag in tags])
        ret['tags'] = tags

    if user_id:
        user = User.query.filter(User.id == user_id).first()
        ret['user'] = user

    return ret


if __name__ == '__main__':
    app.run()
