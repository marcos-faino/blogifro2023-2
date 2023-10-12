from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('listar/', views.PostsListView.as_view(), name='listarposts'),
    path('detalhe/<id>/<slug>', views.DetalhePostView.as_view(), name='detalhepost'),
    path('enviar/<int:pk>/', views.EnviarPostFormView.as_view(), name='enviarpost'),
    path('comentario/<int:pk>/', views.ComentarioCreateView.as_view(),
         name='comentpost'),
    path('cadusuario/', views.CadUsuarioView.as_view(), name='cadusuario'),
    path('login/', views.LoginUserView.as_view(), name='loginuser'),
    path('logout/', views.LogoutUserView.as_view(), name='logoutuser'),
]