from django.contrib import admin
from .models import User, Location, Shop, Review, Image, AboutImage

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(AboutImage)