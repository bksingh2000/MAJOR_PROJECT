from django.urls import path
from . import views
urlpatterns = [
    path('main', views.index, name='index'),
    path('', views.page, name='page'),
    path('attendence', views.take_attendence, name='take_attendence'),
    path('view', views.show_attendence, name='show_attendence'),
    path('train', views.train, name='train'),
    path('camtrain', views.camtrain, name='camtrain'),
    path('profile', views.update_profile, name='profile'),
    path('confirm', views.markRealAttendence, name='confirm'),
    path('save', views.saveTest, name='Test'),
]