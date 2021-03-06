from django.db.models import Q, OuterRef, Subquery, Case, When
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from .models import Movie, Category, Actor, Genre, Rating, Reviews
from django.views.generic import ListView, DetailView
from .forms import ReviewForm, RatingForm



class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").order_by('year').distinct()

# Теперь мы можем наследовать данный класс в наших views и затем достать эти данные в наших
# шаблонах. Этот подход альтернатива 'get_context_data()' котрый позволяет добавить в наш контекст
# какие - либо данные


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip




class MoviesView(GenreYear, ListView):
    # Список фильмов
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 6

    # template = "movies/movies.html"
    # Если имя шаблона не совпадает с таковым по умолчанию (movie_list)

#  Использование Template tags
# Метод закомментирован вследствие применения метода movie_tag.py для избежания дублирования кода
# ***********************************************************************************************
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     # получаем словарь и заносим в переменную context
    #     context["categories"] = Category.objects.all()
    #     # добавляем ключ categories и в качестве значения внесли queryset всех наших категорий
    #     return context
# ***********************************************************************************************


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"
# Django автоматически присоединяет к имени модели Movie суффикс _detail и это совпадает с нашим именем шаблона
# поэтому template = "movies/movie_detail.html"  не требуется

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        # context["form"] = ReviewForm()
        return context

#  Использование Template tags
# Метод закомментирован вследствие применения метода movie_tag.py (подключается в шаблоне)
# для избежания дублирования кода
# ***********************************************************************************************
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     # получаем словарь и заносим в переменную context
    #     context["categories"] = Category.objects.all()
    #     # добавляем ключ categories и в качестве значения внесли queryset всех наших категорий
    #     return context
# ***********************************************************************************************



class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):    # в поле POST запроса ищем parent  и если его нет то будет None
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())





class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"

########################################################################################
#                           Фильтрация фильмов
########################################################################################

class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 6

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)



class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 6

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context