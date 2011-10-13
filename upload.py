# -*- coding: utf-8 -*-

from flaskext import uploads
from blackboard import app
import uuid

from config import UPLOADDESTINATION, IMAGEEXTENSIONS, FILEEXTENSIONS, \
                    MAXIMAGESIZE, MAXFILESIZE

def initializeUpload(uploadType):
    if uploadType == 'images':
        uploadDestination = UPLOADDESTINATION + 'images/'
        UploadSet = uploads.UploadSet('images', IMAGEEXTENSIONS, \
                            lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    elif uploadType == 'files':
        uploadDestination = UPLOADDESTINATION + 'files/'
        UploadSet = uploads.UploadSet('files', FILEEXTENSIONS, \
                            lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    else:
        # throw an exception
        pass

class Upload():

    def __init__(self, UploadSet):
        if UploadSet == 'images':
            from blackboard import imageUploadSet
            self.UploadSet = imageUploadSet
        elif UploadSet == 'files':
            from blackboard import fileUploadSet
            self.UploadSet = fileUploadSet
        else:
            # throw an exception
            pass

    def save(self, sentfile):
        self.file = sentfile
        self.uniqueFilename()
        self.error = None
        try:
            self.name = self.UploadSet.save(self.file, name=self.name)
        except uploads.UploadNotAllowed:
            self.error = 'Upload fehlgeschlagen: upload nicht erlaubt'

    def url(self):
        return self.UploadSet.url(self.name)

    def uniqueFilename(self):
        self.name = self.file.filename
        if len(self.name) > 32:
            self.name = self.name[ (len(self.name)-32): ]
            
        self.name = uuid.uuid4().hex[:16] + '__' + self.name
        return self.name

def setFileSize(uploadType):
    if uploadType == 'images':
        uploads.patch_request_class(app, MAXIMAGESIZE)
    elif uploadType == 'files':
        uploads.patch_request_class(app, MAXFILESIZE)
    else:
        # throw an exception
        pass
