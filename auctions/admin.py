from django.contrib import admin
from .models import User, Category, Listing, CommentSection, Bid, Auction
# Register your models here.

'''class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'body', 'listing', 'created_on')
    list_filter = ('active', 'created_on')
    
    actions = ['block_comments']

    def block_comments(self, request, queryset):
        queryset.update(active=False)
'''

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(CommentSection)
admin.site.register(Bid)
admin.site.register(Auction)
