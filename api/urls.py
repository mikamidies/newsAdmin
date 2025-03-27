from django.urls import path
from . import views


urlpatterns = [
    path("translations", views.TranslationsView.as_view()),
    path("categories", views.CategoryList.as_view()),
    path("products", views.ProductCategoryList.as_view()),
    path("banners", views.BannerList.as_view()),
    path("media", views.MediaList.as_view()),
    path("sliders", views.SliderList.as_view()),
    path("application/create", views.ApplicationView.as_view()),
    path("news", views.NewsList.as_view()),
    path("videos", views.VideosListView.as_view()),
    path("audios", views.AudiosListView.as_view()),
    path("books", views.BooksListView.as_view()),
]
