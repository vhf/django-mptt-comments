from django.contrib import admin
from django.contrib.comments import get_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.contenttypes.models import ContentType


class MpttCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
         {'fields': ('content_type', 'object_pk', 'parent', 'site')}
         ),
        (_('Content'),
         {'fields': ('user', 'title', 'comment')}
         ),
        (_('Metadata'),
         {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
         )
    )

    raw_id_fields = (
        'parent', 'user')  # We don't really want to get huge <select> with all the comments, users...
    list_display = ('title', 'user', 'getobject', 'level',
                    'ip_address', 'submit_date', 'is_public', 'not_is_removed')
    list_filter = ('submit_date', 'is_public', 'is_removed')
    date_hierarchy = None
    list_per_page = 40
    ordering = ('-submit_date',)
    search_fields = ('comment', 'user__username',
                     'user_name', 'user_email', 'user_url', 'ip_address')

    def not_is_removed(self, obj):
        return not obj.is_removed
    not_is_removed.boolean = True
    not_is_removed.short_description = _('Not removed')

    def getobject(self, obj):
        try:
            object_type = ContentType.objects.get(model=str(obj.content_type))
            o = object_type.get_object_for_this_type(pk=str(obj.object_pk))
        except:
            o = "%s : %s" % (obj.content_type, obj.object_pk)
        return o
    getobject.short_description = _('Object')

try:
    admin.site.unregister(Comment)
except:
    pass
admin.site.register(get_model(), MpttCommentsAdmin)
