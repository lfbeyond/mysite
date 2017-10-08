from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,render_to_response
from .models import *
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .commons import cache_manager
from django.contrib.auth.decorators import login_required
import markdown2
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def post_list(request):
    postsAll = Article.objects.annotate(num_comment=Count('id')).filter(
        published_date__isnull=False).order_by('-published_date')
    for p in postsAll:
        p.click = cache_manager.get_click(p)
    paginator = Paginator(postsAll, 5)  # Show 10 contacts per page
    page = request.GET.get('page')
    posts = []
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    finally:
        for pp in posts:
            pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
            pp.user=pp.author
            print(pp.user)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})

from django.shortcuts import render, get_object_or_404

def post_detail(request, pk):
    post = get_object_or_404(Article, pk=str(pk))
    post.text = markdown2.markdown(post.text, extras=['fenced-code-blocks'], )
    post.user=post.author
    if post.published_date == None:
        return render(request, 'blog/post_detail.html', {'post': post})
    else:
        postsAll = Article.objects.annotate(num_comment=Count('id')).filter(
            published_date__isnull=False).order_by('-published_date')
        page_list = list(postsAll)
        print(page_list)
        if post == page_list[-1]:
            before_page = page_list[-2]
            after_page = None
        elif post == page_list[0]:
            before_page = None
            after_page = page_list[1]
        else:
            situ = page_list.index(post)
            before_page = page_list[situ-1]
            after_page = page_list[situ+1]
        return render(request, 'blog/post_detail.html',
                      {'post': post, 'before_page': before_page, 'after_page': after_page})

from .forms import ArticleForm
from django.shortcuts import redirect
#@login_required
@csrf_exempt
def post_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/post_edit.html', {'form': form})




def post_draft_list(request):
    posts = Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    for pp in posts:
        pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_edit(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    return redirect('post_list')

from django.http import Http404

def archives(request):
    try:
        post_list = Article.objects.all().filter(published_date__isnull=False).order_by('-published_date')
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'blog/archives.html', {'post_list': post_list, 'error': False})

def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag).filter(published_date__isnull=False).order_by('-published_date')
        for pp in post_list:
            pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/tag.html', {'post_list' : post_list})

def about_me(request):
    return render(request, 'blog/aboutme.html')

def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'blog/post_list.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0 :
                return render(request, 'blog/search.html', {'post_list': post_list, 'error': True})
            else:
                for pp in post_list:
                    pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
                return render(request, 'blog/search.html', {'post_list': post_list, 'error': False})

    return redirect('/')

def search_user(request, user_id):
    try:
        post_list = Article.objects.filter(author_id=user_id).filter(published_date__isnull=False).order_by('-published_date')
        print(post_list)
        for pp in post_list:
            pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/search_user.html', {'post_list' : post_list})


from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。

from .forms import UserForm

#注册
@csrf_exempt
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)
            if user:
                context['userExit']=True
                return render(req, 'register.html', context)


            #添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #添加到session
            req.session['username'] = username
            #调用auth登录
            auth.login(req, user)
            #重定向到首页
            return redirect('/')
    else:
        context = {'isLogin':False}
    #将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return  render(req,'blog/register.html',context)

#登陆
@csrf_exempt
def login_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #获取的表单数据与数据库进行比较
            user = authenticate(username = username,password = password)
            if user:
                #比较成功，跳转index
                auth.login(req,user)
                req.session['username'] = username
                return  redirect('/')
            else:
                #比较失败，还在login
                context = {'isLogin': False,'pawd':False}
                return render(req, 'login.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(req, 'blog/login.html', context)

#登出
def logout_view(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/')