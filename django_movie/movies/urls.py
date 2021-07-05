from django.urls import path

from .views import *



urlpatterns = [
    path("", MoviesView.as_view(), name='index'),     # v1.0
    path("filter/", FilterMoviesView.as_view(), name='filter'),
    path("json-filter/", JsonFilterMoviesView.as_view(), name='json_filter'),
            # name='json_filter' используем в sidebar.html
    path("search/", Search.as_view(), name='search'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorView.as_view(), name="actor_detail"),
]