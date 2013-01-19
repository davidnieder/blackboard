# -*- coding: utf-8 -*-

import os
import uuid
from werkzeug import secure_filename
from flask import request, url_for

import config
import exceptions
from base import app


upload_directory = config.get('upload_destination')

class NewUpload():

    def __init__(self):
        if request.files.has_key('file'):
            self.file = request.files['file']
        else:
            raise exceptions.UploadFailed('No file given or bad request')

        self.allowed_extensions = config.get('file_extensions', list)
        self.filename = self.file.filename.rsplit('.', 1)[0]
        self.file_extension = self.file.filename.rsplit('.', 1)[1]

        self.file_is_allowed()
        self.unique_filename()

    def save(self):
        self.filepath = os.path.join(upload_directory, self.filename)
        try:
            self.file.save(self.filepath)
        except IOError:
            raise exceptions.UploadFailed('Can\'t save file due to io error')

        self.url = url_for('serve_uploaded_file', filename=self.filename,
                           _external=True)

    def unique_filename(self):
        self.filename = secure_filename(self.filename)
        if len(self.filename) > 46:
            self.filename = self.filename[:46]
        self.filename = self.filename + '__' + uuid.uuid4().hex[:16] + '.' + \
                        self.file_extension

    def file_is_allowed(self):
        if self.file_extension not in self.allowed_extensions:
            raise exception.UploadFailed('File extension not allowed')        

