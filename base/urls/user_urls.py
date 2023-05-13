from django.urls import path
from base.views import user_views as views




urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('register', views.registerUser, name="register"),
    path('profile/update', views.updateUserProfile, name="user-profile-update"),


    path('profile/', views.getUserProfile, name="users-profile"),
    path('', views.getUsers, name="users"),
    path('<str:pk>/delete', views.deleteUser, name="user-delete"),
    path('<str:pk>', views.getUserById, name="user"),
    path('<str:pk>/update', views.updateUser, name="user-update"),


]