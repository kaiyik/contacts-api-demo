from . import views
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('people/', csrf_exempt(
        views.PeopleAPIView.as_view()), name='peopleview'),
    path(
        'people/<int:id>/contacts',
        csrf_exempt(views.ContactAPIView.as_view()),
        name='insertcontactpeople'),
    re_path(
        r'^contacts$',
        csrf_exempt(views.ContactAPIView.as_view()),
        name='contactsearch'),
]
