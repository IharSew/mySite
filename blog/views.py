from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    object_list = Post.published.all()
    # инициализируем объект класса Paginator, указав количество объектов
    # на одной странице:
    paginator = Paginator(object_list, 3)
    # извлекаем из запроса GET параметр Page:
    page = request.GET.get('page')
    try:
        # получаем список объектов на нужной странице с помощью метода page()
        # класса Paginator;
        posts = paginator.page(page)
    except PageNotAnInteger:
        # если указанный параметр page не является целым числом, обращаемся
        # к первой странице. Если page больше, чем общее количество страниц, то
        # возвращаем последнюю:
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/detail.html', {'post': post})
