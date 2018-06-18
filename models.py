# encoding: utf-8

from exts import db
from datetime import datetime


# 笔记与标签的中间表
note_tag = db.Table('note_tag',
                       db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
                       db.Column('tag', db.String(100), db.ForeignKey('tag.tag'), primary_key=True))


# 笔记模型
class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行的时间 传递的是结果
    # now 获取的是 每次创建模型的时间 传递的是方法
    create_time = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag', secondary=note_tag, backref=db.backref('notes', order_by=(id.desc(), create_time.desc())))


# 标签模块
class Tag(db.Model):
    __tablename__ = 'tag'
    tag = db.Column(db.String(100), primary_key=True)
    text = db.Column(db.String(200), nullable=False)


# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    phoneno = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    adminflg = db.Column(db.String(1), nullable=True)


# 留言
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行的时间 传递的是结果
    # now 获取的是 每次创建模型的时间 传递的是方法
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    # 该提问的作者 反向是该作者的所有提问
    user = db.relationship('User', backref=db.backref('messages', order_by=(id.desc(), create_time.desc())))
    note = db.relationship('Note', backref=db.backref('messages', order_by=(id.desc(), create_time.desc())))


# 回答
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    # now()获取的是服务器第一次运行的时间 传递的是结果
    # now 获取的是 每次创建模型的时间 传递的是方法
    create_time = db.Column(db.DateTime, default=datetime.now)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 该回答的作者 反向是该作者的所有回答
    user = db.relationship('User', backref=db.backref('answers'))
    # 该回答的问题 反向 是该问题的所有回答
    message = db.relationship('Message', backref=db.backref('answers', order_by=(id.desc(), create_time.desc())))


