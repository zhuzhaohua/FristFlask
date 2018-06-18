# encoding: utf-8

from flask import redirect, url_for, session
from functools import wraps


# 登录限制的装饰器
# 如果没有登录 则强制调转登录画面
def login_required(func):
    # 如果不加wraps 会导致返回的函数类型发生改变
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
