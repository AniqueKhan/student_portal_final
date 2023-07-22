from django.urls import path
from direct.views import *

urlpatterns = [
    path('', inbox, name='inbox'),
    path("direct/<username>",direct,name='direct'),
    path("send_direct",send_direct,name='send_direct'),
    path('search/', search, name='search'),
    path("new_conversation/<username>",new_conversation,name='new-conversation'),

]