#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import socket
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, Response


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = '/Users/sunteng/PycharmProjects/home-page/image/'
upload_blueprint = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@upload_blueprint.route('/upload', methods=['POST'])
def upload_image():
    req_file = request.files['file']
    if req_file and allowed_file(req_file.filename):
        d = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        filename = req_file.filename.split('.')[0] + '-' + d + '.' + req_file.filename.split('.')[1]
        req_file.save(os.path.join(UPLOAD_FOLDER, filename))
        #return redirect(url_for('upload.uploaded_file',
        #                       filename=filename))
        url = url_for('upload.uploaded_file', filename=filename)
        ip_addr = socket.gethostbyname(socket.gethostname())
        image_url = 'http://' + ip_addr + ':8999' + url
        resp = '{"code": 0, "image": "%s"}' % image_url
        return resp, 200
    return '{"code": 1, "message": "wrong file suffix"}', 500


@upload_blueprint.route("/download/<filename>", methods=['GET'])
def uploaded_file(filename):
    f = file('/Users/sunteng/PycharmProjects/home-page/image/' + filename)
    resp = Response(f, mimetype='image/jpeg')
    return resp, 200
