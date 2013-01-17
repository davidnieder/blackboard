# -*- conding: utf-8 -*-

import lxml
from lxml.html.clean import Cleaner, clean_html

import config
import exceptions



post_rules = {
        'scripts': True,
        'javascript': True,
        'comments': True,
        'style': False,
        'links': False,
        'meta': True,
        'page_structure': True,
        'processing_instructions': True,
        'embedded': False,
        'frames': False,
        'forms': False,
        'annoying_tags': False,
        'remove_unknown_tags': False,
        'safe_attrs_only': True,
        'add_nofollow': False
}

allowed_comment_tags = ['a', 'b', 'i', 's', 'u', 'strike', 'strong', 'quote', \
                        'ul', 'li', 'dl', 'dt', 'dd']

comment_rules = {
        'scripts': True,
        'javascript': True,
        'comments': True,
        'style': True,
        'links': False,
        'meta': True,
        'page_structure': True,
        'processing_instructions': True,
        'embedded': True,
        'frames': True,
        'annoying_tags': True,
        'remove_unknown_tags': False,
        'safe_attrs_only': True,
        'add_nofollow': True,
        'allow_tags': allowed_comment_tags
}


class ValidatePostForm():

    def __init__(self, input):
        self.title = input.get('post_title')
        self.content = input.get('post_content')
        self.category = input.get('post_category')
        self.is_public = input.get('post_is_public')

        if self.is_public:
            self.is_public = True
        else:
            self.is_public = False

        if self.category not in config.get('post_categories'):
            raise exceptions.CantValidateForm

        if self.title:
            # strip markup
            html_string = lxml.html.fromstring(self.title)
            self.title = unicode(html_string.text_content())
        else:
            self.title = ''

        if self.content:
            # clean markup
            cleaner = Cleaner(**post_rules)
            self.content = cleaner.clean_html(self.content)
            # replace newlines
            self.content = self.content.replace('\r\n', '<br />')
        else:
            raise exceptions.CantValidateForm


class ValidateCommentForm():

    def __init__(self, input):
        self.content = input.get('content')
        self.related_post = input.get('related_post')

        if self.related_post:
            try:
                self.related_post = int(self.related_post)
            except:
                raise exceptions.CantValidateForm
        else:
            raise exceptions.CantValidateForm

        if self.content:
            # clean html
            cleaner = Cleaner(**comment_rules)
            self.content = cleaner.clean_html(self.content)
            # replace newlines
            self.content = self.content.replace('\r\n', '<br />')
        else:
            raise exceptions.CantValidateForm

