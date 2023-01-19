from django.contrib import admin

from .models import Hotel, Food, Blogger, Post, Tag, ReviewPost, HotelImage

admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Food)
admin.site.register(Blogger)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(ReviewPost)
