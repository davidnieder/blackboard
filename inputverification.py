class NewPostForm():

    def __init__(self, form):
        self.form = form
        post = self.form['contenttype']

        if post ==  'text':
            self.verify = self.textpost()
        elif post == 'audio':
            self.verify = self.audiopost()
        elif post == 'video':
            self.verify = self.videopost()
        elif post == 'image':
            self.verify = self.imagepost()
        elif post == 'link':
            self.verify = self.linkpost()
        else:
            self.verify = False

    def textpost(self):
        return True

    def audiopost(self):
        return True

    def videopost(self):
        return True

    def imagepost(self):
        return True

    def linkpost(self):
        return True

class NewCommentForm():

    def __init__(self, form):
        if form['relatedpost']:
            self.relatedpost = form['relatedpost'];
        else:
            self.relatedpost = False;

        if form['comment']:
            self.comment = form['comment'];
        else:
            self.comment = False;

        self.verify = self.relatedpost and self.comment

