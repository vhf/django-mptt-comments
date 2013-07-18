from django.contrib.comments import get_model
from django.contrib.comments.forms import CommentForm
from django.utils.translation import ugettext_lazy as _
from django import forms
import time
from mptt_comments.models import MpttComment


class MpttCommentForm(CommentForm):
    parent_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__(self, target_object, parent_comment=None, data=None, initial=None):
        self.parent_comment = parent_comment
        super(MpttCommentForm, self).__init__(
            target_object, data=data, initial=initial)

        self.fields.keyOrder = [
            'comment',
            'honeypot',
            'content_type',
            'object_pk',
            'timestamp',
            'security_hash',
            'parent_pk'
        ]

    def get_comment_model(self):
        """
        Get the comment model to create with this form. Subclasses in custom
        comment apps should override this, get_comment_create_data, and perhaps
        check_for_duplicate_comment to provide custom comment models.
        """
        return MpttComment

    def get_comment_create_data(self):
        """
        Returns the dict of data to be used to create a comment. Subclasses in
        custom comment apps that override get_comment_model can override this
        method to add extra fields onto a custom comment model.
        """

        data = super(MpttCommentForm, self).get_comment_create_data()
        parent_comment = None
        parent_pk = self.cleaned_data.get("parent_pk")
        if parent_pk:
            parent_comment = get_model().objects.get(pk=parent_pk)
        data.update({
            'is_public': parent_comment and parent_comment.is_public or True,
            'parent': parent_comment
        })

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict = {
            'content_type': str(self.target_object._meta),
            'object_pk': str(self.target_object._get_pk_val()),
            'timestamp': str(timestamp),
            'security_hash': self.initial_security_hash(timestamp),
            'parent_pk': self.parent_comment and str(self.parent_comment.pk) or ''
        }

        return security_dict
