#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import socket
from datetime import datetime
from flask import Blueprint, request, url_for, Response
from utils.auth_utils import ba


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = '/opt/home_page/home_page/image/'
upload_blueprint = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload_blueprint.route('/images', methods=['POST'])
@ba.authorize
def upload_image():
    req_file = request.files['file']
    if req_file and allowed_file(req_file.filename):
        d = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        filename = req_file.filename.split('.')[0] + '-' + d + '.' + req_file.filename.split('.')[1]
        req_file.save(os.path.join(UPLOAD_FOLDER, filename))
        url = url_for('upload.uploaded_file', filename=filename)
        ip_addr = socket.gethostbyname(socket.gethostname())
        image_url = 'http://' + '47.96.190.33' + ':8999' + url
        resp = '{"code": 0, "image": "%s"}' % image_url
        return resp, 200
    return '{"code": 1, "message": "wrong file suffix"}', 500


@upload_blueprint.route("/image/<string:filename>", methods=['GET'])
@ba.authorize
def uploaded_file(filename):
    f = file('/opt/home_page/home_page/image/' + filename)
    resp = Response(f, mimetype='image/jpeg')
    return resp, 200
