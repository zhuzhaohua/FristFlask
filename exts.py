# encoding: utf-8

from flask_sqlalchemy import SQLAlchemy
from html.parser import HTMLParser


# 创建DB对象 全局使用
db = SQLAlchemy()

main_url = "http://127.0.0.1:5000/"


def html_unescape(content):
    html_parser = HTMLParser()
    html = html_parser.unescape(content)
    return html