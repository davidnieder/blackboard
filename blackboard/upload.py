# -*- coding: utf-8 -*-

import uuid

from flaskext import uploads

from base import app
import exceptions
import config


def initializeUpload(uploadType):
    if uploadType == 'images':
        uploadDestination = config.get('upload_destination') + 'images/'
        UploadSet = uploads.UploadSet('images', config.get('image_extensions',
                            tuple), lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    elif uploadType == 'files':
        uploadDestination = config.get('upload_destination') + 'files/'
        UploadSet = uploads.UploadSet('files', config.get('file_extensions',
                            tuple), lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    elif uploadType == 'avatars':
        uploadDestination = config.get('upload_destination') + 'avatars/'
        UploadSet = uploads.UploadSet('avatars', config.get('image_extensions',
                            tuple), lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    elif uploadType == 'audio':
        uploadDestination = config.get('upload_destination') + 'audio/'
        UploadSet = uploads.UploadSet('audio', config.get('audio_extensions',
                            tuple), lambda dest: uploadDestination)
        uploads.configure_uploads(app, UploadSet)
        return UploadSet
    else:
        raise exceptions.CantCreateUploadSet()


class Upload():

    def __init__(self, UploadSet):
        if UploadSet == 'images':
            from base import imageUploadSet
            self.UploadSet = imageUploadSet
        elif UploadSet == 'files':
            from base import fileUploadSet
            self.UploadSet = fileUploadSet
        elif UploadSet == 'avatars':
            from base import avatarUploadSet
            self.UploadSet = avatarUploadSet
        elif UploadSet == 'audio':
            from base import audioUploadSet
            self.UploadSet = audioUploadSet
        else:
            raise exceptions.NoSuchUploadSet

    def save(self, sentfile):
        self.file = sentfile
        self.uniqueFilename()
        try:
            self.name = self.UploadSet.save(self.file, name=self.name)
        except uploads.UploadNotAllowed:
            raise exceptions.UploadFailed

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
        uploads.patch_request_class(app, config.get('max_image_size', int))
    elif uploadType == 'files':
        uploads.patch_request_class(app, config.get('max_file_size', int))
    elif uploadType == 'avatars':
        uploads.patch_request_class(app, config.get('max_avatar_size', int))
    elif uploadType == 'audio':
        uploads.patch_request_class(app, config.get('max_audio_size', int))
    else:
        raise exceptions.NoSuchUploadSet()

