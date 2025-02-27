from django.urls import path
from . import views
from .api.TeamReviewsByName import TeamReviewsByName
from .api.TeamVideosByName import TeamVideosByName
from .api.TeamDetail import TeamDetail
from .api.TeamList import TeamList
from .api.ReviewDetail import ReviewDetail
from .api.ReviewList import ReviewList
from .api.YoutubeVideoDetail import YoutubeVideoDetail
from .api.YoutubeVideoList import YoutubeVideoList

urlpatterns = [
    path('', views.team_list,name='team_list'),
    path('<str:team>/', views.selected_team, name='selected_team'),
    path('create/team',views.create_team,name='create_team'),
    path('create/video',views.create_video,name='create_video'),
    path('news/<str:team_name>',views.get_team_info,name='get_team_info'),
    path('create/review',views.create_review,name='create_review'),
    path('data/api/',TeamList.as_view(),name='teams'),
    path('data/api/<int:id>',TeamDetail.as_view(),name='team_by_id'),
    path('review/data/api',ReviewList.as_view(),name='reviews'),
    path('review/data/api/<int:id>',ReviewDetail.as_view(),name='review_by_id'),
    path('data/api/reviews',TeamReviewsByName.as_view(),name='review_by_team_name'),
    path('data/api/videos',TeamVideosByName.as_view(),name='videos_by_team_name'),
    path('video/data/api',YoutubeVideoList.as_view(),name='videos'),
    path('video/data/api/<int:id>',YoutubeVideoDetail.as_view(),name='video_by_id'),
]

