from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm


class PostListView(ListView):
    # использовать переопределенный QuerySet модели:
    queryset = Post.published.all()
    # использовать posts в качестве переменной контекста HTML-шаблона,
    # в которой будет храниться список объектов. Если не указать атрибут context_object_name,
    # по умолчанию используется переменная object_list;
    context_object_name = 'posts'
    # использовать постраничное отображение по три объекта на странице;
    paginate_by = 3
    # использовать указанный шаблон для формирования страницы. Если бы
    # мы не указали template_name, то базовый класс ListView использовал бы
    # шаблон blog/post_list.html.
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


