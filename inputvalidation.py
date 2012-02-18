# _*_ conding: UTF-8 _*_

import lxml
from lxml.html.clean import Cleaner, clean_html

import exceptions

allowed_video_sites = ['youtube.com',
                       'www.youtube.com',
                       'vimeo.com',
                       'player.vimeo.com',
                       'video.google.com']

allowed_audio_sites = ['soundcloud.com',
                       'player.soundcloud.com']
allowed_audio_sites += allowed_video_sites

allowed_embedding_tags = ['iframe', 'embed', 'object']
allowed_text_tags = ['a', 'b', 'i', 's', 'u', 'strike', 'strong', 'br', 'span', 'div']

video_rules = {
            'host_whitelist': allowed_video_sites,
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
            'forms': True,
            'annoying_tags': True,
            'remove_unknown_tags': True,
            'safe_attrs_only': True,
            'add_nofollow': True,
            'whitelist_tags': set(allowed_embedding_tags)
        }

audio_rules = {
            'host_whitelist': allowed_audio_sites,
            'scripts': True,
            'javascript': True,
            'comments': True,
            'style': True,
            'links': True,
            'meta': True,
            'page_structure': True,
            'processing_instructions': True,
            'embedded': True,
            'frames': True,
            'forms': True,
            'annoying_tags': True,
            'remove_unknown_tags': False,
            'safe_attrs_only': True,
            'add_nofollow': True,
            'whitelist_tags': set(allowed_embedding_tags),
            'allow_tags': ['audio']
        }

text_rules = {
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
            'forms': True,
            'annoying_tags': True,
            'remove_unknown_tags': False,
            'safe_attrs_only': True,
            'add_nofollow': True,
            'allow_tags': allowed_text_tags 
        }

class NewPostForm():

    def __init__(self, form):
        self.form = form
        self.validated_form = dict( title   = '',
                                    content = '',
                                    comment = '',
                                    code    = '' )

        if not self.form.has_key('contenttype'):
            raise exceptions.CantValidateForm

        if self.form['contenttype'] == 'audio':
            self.validate_audio()
        elif self.form['contenttype'] == 'video':
            self.validate_video()
        elif self.form['contenttype'] == 'image':
            self.validate_image()
        elif self.form['contenttype'] == 'link':
            self.validate_link()
        elif self.form['contenttype'] == 'text':
            self.validate_text()
        else:
            raise exceptions.CantValidateForm

        self.validated_form['contenttype'] = self.form['contenttype']

        # if this post has a title: strip markup
        self.strip_html_in_title_field()
        # if this post has a comment: clean markup
        self.clean_html_in_comment_field()

        if self.field_has_content('public_post'):
            if self.form['public_post'] == '1':
                self.validated_form['public_post'] = True
            else:
                self.validated_form['public_post'] = False
        else:
            self.validated_form['public_post'] = False


    def validate_audio(self):
        # no embedding code?
        if not self.field_has_content('code'):
            raise exceptions.CantValidateForm

        # clean html in code field
        cleaner = Cleaner(**audio_rules)
        self.validated_form['code'] = cleaner.clean_html(self.form['code'])


    def validate_video(self):
        # no embedding code?
        if not self.field_has_content('code'):
            raise exceptions.CantValidateForm

        # clean html in code field
        cleaner = Cleaner(**video_rules)
        self.validated_form['code'] = cleaner.clean_html(self.form['code'])


    def validate_image(self):
        # same validation as for links
        self.validate_link()

    def validate_link(self):
        # no link in a link post?
        if not self.field_has_content('link'):
            raise exceptions.CantValidateForm

        # link should just be an url/uri, strip all html
        self.validated_form['link'] = self.strip_html(self.form['link'])

        # url starts not with http:// or https:// ?
        if self.validated_form['link'][:7] != 'http://' and \
           self.validated_form['link'][:8] != 'https://':
            raise exceptions.CantValidateForm

    def validate_text(self):
        # no text in a text post?
        if not self.field_has_content('content'):
            raise exceptions.CantValidateForm

        # workaround a lxml bug
        html_string = '<span>' + self.form['content'] + '</span>'

        # clean content field html
        cleaner = Cleaner(**text_rules)
        self.validated_form['content'] = cleaner.clean_html(html_string)


    def field_has_content(self, key):
        if not self.form.has_key(key):
            return False
        if not self.form[key]:
            return False

        return True

    def strip_html(self, html_string):
        ''' Get rid of all markup '''
        html_string = lxml.html.fromstring(html_string)

        return unicode(html_string.text_content())

    def strip_html_in_title_field(self):
        if self.field_has_content('title'):
            title = self.strip_html(self.form['title'])
            self.validated_form['title'] = title

    def clean_html_in_comment_field(self):
        if self.field_has_content('comment'):
            # workaround to be compatible with older lxml versions:
            html_string = '<span>' + self.form['comment'] + '</span>'

            cleaner = Cleaner(**text_rules)
            self.validated_form['comment'] = \
                cleaner.clean_html(html_string)

class NewCommentForm(NewPostForm):

    def __init__(self, form):
        self.form = form
        self.validated_form = {}

        if not self.field_has_content('comment'):
            raise exceptions.CantValidateForm

        cleaner = Cleaner(**text_rules)
        self.validated_form['comment'] = cleaner.clean_html(self.form['comment'])

        if not self.field_has_content('relatedpost'):
            raise exceptions.CantValidateForm
        else:
            try:
                post_id = int(self.form['relatedpost'])
                self.validated_form['relatedpost'] = post_id
            except:
                raise exceptions.CantValidateForm

    def get_comment(self):
        return self.validated_form['comment']

    def get_related_post_id(self):
        return self.validated_form['relatedpost']

