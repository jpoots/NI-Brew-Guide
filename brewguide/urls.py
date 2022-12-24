from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name='contact'),
    path("search/", views.search, name='search'),
    path("shop/<str:name>", views.shop, name="shop"),
    path("best/", views.best, name="best"),
    path("review/", views.review, name="review")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)