from django.contrib.auth.views import LoginView
from django.urls import path, include
from .controllers import UtilsController, AdminController
from .controllers import (
    translations, ProductController,
    CategoryController, BannerController,
    SliderContoller, MediaController,
    ApplicationController, NewsController, VideosController, AudiosController, BooksController
)
from .controllers import LangsController
from admins.controllers.NewsController import news_router


urlpatterns = [
    path('login', LoginView.as_view(
        template_name='admin/sing-in.html',
        success_url='/admin/',
    ), name='login_admin'),

    path("", UtilsController.home_view, name="home"),
    path("images/save", UtilsController.save_images, name="images_save"),
    path("images/delete", UtilsController.delete_image, name="del-img"),
    path("delete_model_field", UtilsController.delete_model_image,
         name="delete_model_field"),
    path("delete", UtilsController.delete_item, name='delete'),
    path('admins', AdminController.AdminsList.as_view(), name='admin_list'),
    path("admins/create", AdminController.AdminCreate.as_view(),
         name='admins_create'),
    path("admins/<int:pk>/edit",
         AdminController.AdminUpdate.as_view(), name='admins_edit'),
    path('logout', UtilsController.logout_view, name='logout_url'),


    # langs
    path('langs', LangsController.LangsList.as_view(), name='langs_list'),
    path('langs/create', LangsController.LngCreateView.as_view(),
         name='create_lang'),
    path('langs/<int:pk>/edit',
         LangsController.LangsUpdate.as_view(), name='lang_update'),
    path('langs/delete', LangsController.delete_langs, name='lang_del'),


    # translations
    path('translations', translations.TranslationList.as_view(),
         name='translation_list'),

    path("translations/<int:pk>",
         translations.TranslationGroupDetail.as_view(),
         name='transl_group_detail'),

    path('translation/edit', translations.translation_update,
         name='translation_edit'),

    path("translations/<int:pk>/edit",
         translations.TranslationGroupUdpate.as_view(),
         name='transl_group_edit'),

    path("translations/<int:pk>/delete",
         translations.delete_translation, name='transl_del'),

    path("translation_group/create", translations.add_trans_group,
         name='transl_group_create'),

    path("translations/import", translations.translations_from_json,
         name="translation_import"),
]


urlpatterns += BannerController.banner_router.paths
urlpatterns += CategoryController.category_router.paths
urlpatterns += ProductController.product_router.paths
urlpatterns += SliderContoller.slider_router.paths
urlpatterns += MediaController.media_router.paths
urlpatterns += ApplicationController.application_router.paths
urlpatterns += NewsController.news_router.paths
urlpatterns += VideosController.videos_router.paths
urlpatterns += AudiosController.audios_router.paths
urlpatterns += BooksController.books_router.paths