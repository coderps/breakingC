from django.urls import path
from bc.views import *

urlpatterns = [
    # GET
    path('stuffs/', StuffApiView.as_view()),
    path('stuff-records/', HistoryApiView.as_view()),
    path('rooms/', RoomsApiView.as_view()),
    path('vacations/', VacationAPIView.as_view()),
    path('stats/avg/', AvgAPIView.as_view()),
    path('stats/totals/', TotalAPIView.as_view()),
    # POST
    path('store-records', StuffRecordApiView.as_view())
]
