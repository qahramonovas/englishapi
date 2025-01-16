from django.urls import path

from apps.views import CustomTokenObtainPairView, CustomTokenRefreshView, SendEmailAPIView, CodeUserAPIView, \
    RegisterUserCreateAPIView, VocabCreateAPIView, UnitListAPIView, UnitUpdateAPIView, UnitDeleteAPIView, \
    UnitCreateAPIView, UnitSearchListAPIView, UnitFilterListAPIView, BookListAPIView, BookUpdateAPIView, \
    BookDeleteAPIView, BookCreateAPIView, VocabFilterListAPIView, VocabularyUpdateAPIView, VocabDeleteAPIView, \
    VocabListAPIView, BookSearchListAPIView, BookInfoAPIView, UnitInfoAPIView, VocabInfoAPIView, VocabTryWordAPIView, \
    VocabCheckWordAPIView, VocabTestAPIView, VocabTestCheckAPIView

urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view()),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view()),
    path('auth/register', RegisterUserCreateAPIView.as_view()),
    path('auth/send/verify', CodeUserAPIView.as_view()),
    path('auth/send/mail', SendEmailAPIView.as_view()),
    path('vocab/create', VocabCreateAPIView.as_view()),
    path('vocab/info/<int:pk>', VocabInfoAPIView.as_view()),

]

# ==================================

urlpatterns += [
    path('unit/list', UnitListAPIView.as_view()),
    path('unit/<int:pk>/update/', UnitUpdateAPIView.as_view()),
    path('unit/<int:pk>/delete/', UnitDeleteAPIView.as_view()),
    path('unit/create', UnitCreateAPIView.as_view()),
    path('unit/search', UnitSearchListAPIView.as_view()),
    path('unit/filter/<int:book_id>', UnitFilterListAPIView.as_view()),
    path('unit/info/<int:pk>', UnitInfoAPIView.as_view()),

]

# ===================================

urlpatterns += [
    path('book/list', BookListAPIView.as_view()),
    path('book/<int:pk>/update/', BookUpdateAPIView.as_view()),
    path('book/<int:pk>/delete/', BookDeleteAPIView.as_view()),
    path('book/create', BookCreateAPIView.as_view()),
    path('book/search', BookSearchListAPIView.as_view()),
    path('book/info/<int:pk>', BookInfoAPIView.as_view()),

]

# =====================================


urlpatterns += [
    path('vocab/create', VocabCreateAPIView.as_view()),
    path('vocab/update', VocabularyUpdateAPIView.as_view()),
    path('vocab/list', VocabListAPIView.as_view()),
    path('vocab/delete', VocabDeleteAPIView.as_view()),
    path('vocab/filter/<int:unit_id>', VocabFilterListAPIView.as_view()),
]

urlpatterns += [
    path('unit/vocab/to_try', VocabTryWordAPIView.as_view()),
    path('unit/vocab/check', VocabCheckWordAPIView.as_view()),
    path('unit/test/filter', VocabTestAPIView.as_view()),
    path('unit/test/check', VocabTestCheckAPIView.as_view()),

]
