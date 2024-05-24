from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>',views.profile_page,name='myprofile'),
    path('<slug:slug>/editdp',views.edit_image,name='editdp'),
    path('<slug:slug>/deletedp',views.remove_pic,name='removedp'),
    path('<slug:slug>/about',views.update_about,name='updateabout'),
    path('<slug:slug>/post/addnew/', views.create_post, name='addpost'), 
    path('<slug:slug>/posts/<int:post_id>', views.post_detail, name='postdetail'),
    path('<slug:slug>/posts/<int:post_id>/like', views.like_post, name='likepost'),
    path('user/<int:user_id>/add_friend/', views.add_friend, name='addfriend'),
    path('user/<int:user_id>/remove_friend/', views.remove_friend, name='removefriend'),
    path('<slug:slug>/friends/', views.friend_list, name='friendlist'),
    
]