#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from app.blueprints import data_opt, index_opt, user_opt, upload_opt


app = Flask(__name__)

app.register_blueprint(data_opt.data_blueprint)
app.register_blueprint(user_opt.user_blueprint)
app.register_blueprint(index_opt.index_blueprint)
app.register_blueprint(upload_opt.upload_blueprint)

UPLOAD_FOLDER = '/Users/sunteng/PycharmProjects/home-page/image/'


@app.route("/index", methods=['GET'])
def get_index():
    return render_template("index.html", title="HomePage", user="amyFox")


if __name__ == '__main__':
    # 本机ip 192.168.1.107
    app.run(host='0.0.0.0', port=8999)

