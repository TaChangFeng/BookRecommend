import re
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Book,UserHistory
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import UserHistory
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count
from BookRecommend.models import BookRating,Book,UserHistory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from scipy.sparse import csr_matrix
import numpy as np
import random
from django.http import HttpResponse
from django.template import loader
def hello(request):
    return render(request, 'hello.html')

def get_top_books():
    # 计算每本书的平均评分，并按评分降序排序
    top_books = BookRating.objects.values('ISBN').annotate(avg_rating=Avg('Book_Rating')).order_by('-avg_rating')[:6]
    
    # 输出 top_books 的内容
    print("top_books:", top_books)

    # 获取前9本书的详细信息（标题和URL）
    top_n_books = []
    for book_data in top_books:
        isbn = book_data['ISBN']

        # 如果ISBN等于 '0749314036' 或 '0307105318'，跳过当前循环
        if isbn in ['0749314036', '0307105318']:
            continue

        book_info = Book.objects.filter(ISBN=isbn).first()
        print(f"ISBN: {isbn}, Book Info: {book_info}")  # 添加这行打印语句
        if book_info:
            book_info.avg_rating = book_data['avg_rating']
            top_n_books.append(book_info)

    return top_n_books

def mainpage(request):
    top_books = get_top_books()
    context = {'top_books': top_books}
    return render(request, 'mainpage.html', context)

def loginview(request):
    if request.method == 'GET':
        return render(request, 'loginview.html')  # 渲染登录页面模板

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # 登录成功后的重定向页面，可以根据需求修改
            return HttpResponseRedirect('/mainpage/')  # 或者 return redirect('main')
        else:
            # 如果认证失败，返回错误信息和用户输入的用户名
            error_message = '[系统提示]请输入正确的账号或密码!'
            return render(request, 'loginview.html', {'error_message': error_message, 'username': username})

    return HttpResponse("Invalid Request")

def logout_view(request):
    logout(request)
    # 重定向到某个页面
    return redirect('mainpage')

def zhuce(request):
    error_message = None
    username_error = False
    password_error = False
    confirm_password_error = False

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, password, confirm_password]):
            error_message = "请填写所有字段。"
            if not username:
                username_error = True
            if not password:
                password_error = True
            if not confirm_password:
                confirm_password_error = True
        elif not (username.isdigit() and len(username) > 4):
            error_message = "[系统提示]用户名必须为纯数字且长度大于4。"
        elif not re.match("^(?=.*[a-zA-Z])(?=.*\d).+$", password):
            error_message = "[系统提示]密码必须包含至少一个字母和一个数字。"
        elif password != confirm_password:
            error_message = "[系统提示]密码不匹配，请重新输入。"
        elif User.objects.filter(username=username).exists():
            error_message = "[系统提示]该账号已存在，请选择另一个账号。"
        else:
            # 处理注册逻辑
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('loginview')  # 注册成功后重定向到登录页面

    return render(request, 'zhuce.html', {
        'error_message': error_message,
        'username_error': username_error,
        'password_error': password_error,
        'confirm_password_error': confirm_password_error
    })

def library(request):
    book_list = Book.objects.all()

    # 设置每页显示的数量
    items_per_page = 20
    paginator = Paginator(book_list, items_per_page)

    # 获取当前页码
    page = request.GET.get('page')

    # 获取当前页的图书列表
    books = paginator.get_page(page)

    return render(request, 'library.html', {'books': books})


# 构建用户-书籍评分稀疏矩阵
def create_user_interaction_matrix():
    user_history = UserHistory.objects.all().values_list('user_id', 'book__ISBN')
    user_click_df = pd.DataFrame(list(user_history), columns=['User_ID', 'ISBN'])
    user_click_df['Interaction'] = 1
    user_interaction_matrix = pd.pivot_table(user_click_df, values='Interaction', index='User_ID', columns='ISBN', fill_value=0)
    return csr_matrix(user_interaction_matrix), user_interaction_matrix.index, user_interaction_matrix.columns

# 计算特定用户的相似度
def calculate_similarity(user_interaction_matrix, user_id, user_index):
    if user_id not in user_index:
        return np.array([])

    user_idx = np.where(user_index == user_id)[0][0]
    similarity = cosine_similarity(user_interaction_matrix[user_idx], user_interaction_matrix)
    return similarity[0]

# 找到相似用户
def find_similar_users(similarity, user_id, user_index):
    if similarity.size == 0:
        return np.array([])

    sorted_users = np.argsort(-similarity)
    similar_users = sorted_users[sorted_users != user_id][:5]
    return user_index[similar_users]


def get_random_books(number_of_books=5):
    all_books = list(Book.objects.all())
    return random.sample(all_books, min(number_of_books, len(all_books)))


# 生成推荐书单
def get_recommendations_based_on_clicks(user_id, similar_users, number_of_books=5):
    user_clicked_books = UserHistory.objects.filter(user_id=user_id).values_list('book__ISBN', flat=True)

    # 获取相似用户评分过且目标用户未点击过的书籍的ISBN
    similar_users_books = BookRating.objects.filter(
        User_ID__in=similar_users
    ).exclude(
        ISBN__in=user_clicked_books
    ).values_list('ISBN', flat=True).distinct()

    # 获取推荐书籍
    recommended_books_qs = Book.objects.filter(ISBN__in=similar_users_books)[:number_of_books]
    recommended_books = list(recommended_books_qs)  # 将QuerySet转换为list

    # 如果推荐书籍不足，用随机书籍填补
    if len(recommended_books) < number_of_books:
        needed_books = number_of_books - len(recommended_books)
        all_books_qs = Book.objects.exclude(ISBN__in=user_clicked_books)
        all_books = list(all_books_qs)  # 将QuerySet转换为list
        random_books = random.sample(all_books, min(needed_books, len(all_books)))
        recommended_books.extend(random_books)  # 现在可以使用extend方法

    return recommended_books


def record_and_show_book(request, bid, isbn):
    user_id = request.user.id
    book = get_object_or_404(Book, bid=bid)

    UserHistory.objects.create(user_id=user_id, book_id=book.bid)

    user_interaction_matrix, user_index, book_index = create_user_interaction_matrix()
    similarity = calculate_similarity(user_interaction_matrix, user_id, user_index)

    if similarity.size > 0:
        similar_users = find_similar_users(similarity, user_id, user_index)
        if similar_users.size > 0:
            recommended_books = get_recommendations_based_on_clicks(user_id, similar_users)
        else:
            recommended_books = get_random_books()
    else:
        recommended_books = get_random_books()

    book_ratings = BookRating.objects.filter(ISBN=isbn)
    avg_rating = book_ratings.aggregate(Avg('Book_Rating'))['Book_Rating__avg']
    num_ratings = book_ratings.aggregate(Count('User_ID', distinct=True))['User_ID__count']

    return render(request, 'showbook.html', {
        'book': book,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
        'recommended_books': recommended_books
    })




def search(request):
    query = request.GET.get('q', '')
    book_list = Book.objects.filter(Book_Title__icontains=query)
    
    items_per_page = 10
    paginator = Paginator(book_list, items_per_page)
    page = request.GET.get('page')
    books = paginator.get_page(page)

    return render(request, 'search.html', {'books': books, 'query': query})


def history(request):
    # 获取当前登录用户的id
    user_id = request.user.id

    # 通过用户id从UserHistory表中获取足迹信息
    user_history = UserHistory.objects.filter(user_id=user_id)

    # 通过足迹信息中的book_id获取对应的图书信息
    books = Book.objects.filter(bid__in=user_history.values('book_id'))

    return render(request, 'history.html', {'user_history': user_history, 'books': books})

def about(request):
    return render(request, 'about.html')

@login_required
def grant_admin_access(request):
    # 获取或创建权限对象
    content_type = ContentType.objects.get_for_model(User)
    permission, created = Permission.objects.get_or_create(
        codename='can_access_admin',
        content_type=content_type,
    )

    # 将权限赋予当前登录用户
    request.user.user_permissions.add(permission)

    return render(request, 'grant_admin_access.html')


