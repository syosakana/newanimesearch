from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Anime,Message,Good,Friend,WhoGood
from .forms import MessageForm,HelloForm,FindForm,GenreForm,AuthorForm,ContentForm,SignupForm,LoginForm,UserForm,FindUserForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from janome.tokenizer import Tokenizer
from django_pandas.io import read_frame
import pandas as pd


# Create your views here.

@login_required(login_url='/admin/login/')
def index(request):
    
    #初期画面ビュー
    if request.method =='POST':
        if request.POST['mode'] == '_findform_':
            #タイトルから探せる探索フォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str =request.POST['find']
            data = Anime.objects.filter(title__contains=str).order_by('id').reverse#タイトルが入力された文字を含むレコードを抽出

        
        
        if request.POST['mode'] == '_genreform_':
            #ジャンルから検索出来るフォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str =request.POST['genre']
            data = Anime.objects.filter(genre=str).order_by('id').reverse()

        if request.POST['mode'] == '_authorform_':
            #作者から検索できるフォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str = request.POST['author']
            data = Anime.objects.filter(author=str).order_by('id').reverse()



    else:
        #なにもなかったらのコード
        findform = FindForm()
        genreform = GenreForm()
        authorform = AuthorForm()
        data = Anime.objects.all().order_by('id').reverse()

    pa = {#初期値設定
        'title':'アニメ情報',
        'data' : data,
        'findform':findform,
        'genreform':genreform,
        'authorform':authorform,

    
    }
    return render(request, 'hello/index.html',pa)

def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='/hello/login')

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'hello/signup.html', param)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect(to='/hello')

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, 'hello/login.html', param)

@login_required(login_url='/admin/login/')
def reverse(request,mun=1):
    #登録逆順ビュー
    if request.method =='POST':
        if request.POST['mode'] == '_findform_':
            #タイトルから探せる探索フォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str =request.POST['find']
            data = Anime.objects.filter(title__contains=str)#タイトルが入力された文字を含むレコードを抽出
        
        if request.POST['mode'] == '_genreform_':
            #ジャンルから検索出来るフォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str =request.POST['genre']
            data = Anime.objects.filter(genre=str)

        if request.POST['mode'] == '_authorform_':
            #作者から検索できるフォーム
            findform = FindForm(request.POST)
            genreform = GenreForm(request.POST)
            authorform = AuthorForm(request.POST)
            str = request.POST['author']
            data = Anime.objects.filter(author=str)
                   
    else:
        #なにもなかったらのコード
        findform = FindForm()
        genreform = GenreForm()
        authorform = AuthorForm()
        data = Anime.objects.all()

    pa = {#初期値設定
        'title':'アニメ情報',
        'data' : data,
        'findform':findform,
        'genreform':genreform,
        'authorform':authorform,
    
    }
    return render(request, 'hello/reverse.html',pa)


@login_required(login_url='/admin/login/')
def think(request):

    #アニメに対してのコメントに合った場合のアニメを表示する
    if request.method =='POST':
        if request.POST['mode'] == '_contentform_':
            #から探せる探索フォーム
            contentform = ContentForm(request.POST)
            str = request.POST['content']
            data = Message.objects.filter(content__contains=str).order_by('id').reverse()#タイトルが入力された文字を含むレコードを抽出

            

    else:
        #通常の画面
        contentform = ContentForm()
        data = Message.objects.all().order_by('id').reverse()#.distinct().values_list('Anime')
        
        #コメントが寄せられたもの全て表示される．同じアニメが何件も表示される．
    pa = {#初期値設定
        'title':'感想はこちら',
        'contentform':contentform,
        'data' : data, 

    }

    return render(request, 'hello/think.html',pa)

@login_required(login_url='/admin/login/')
def create(request):
    #アニメ登録画面
    pa = {
        'title':'登録会場',
        'form' : HelloForm(),
    }
    if (request.method == 'POST'):
        title = request.POST['title']
        author = request.POST['author']
        broadcaststart = request.POST['broadcaststart']
        broadcastfinish = request.POST['broadcastfinish']
        genre = request.POST['genre']
        anime = Anime(title=title,author=author,broadcaststart=broadcaststart,broadcastfinish=broadcastfinish, genre=genre)
        anime.save()
        return redirect(to='/hello')
    return render(request,'hello/create.html',pa)

@login_required(login_url='/admin/login/')
def message(request,num):
    (public_user) = get_public()
    #アニメ詳細画面とコメントが記入出来る画面
    post = Anime.objects.get(id=num)#アニメモデルのIDを取得
    data = Anime.objects.all().get(id=num)
    dict_polarity = {}
    with open('/home/kanata/ei/hello/pn_ja.txt', 'r') as f:
        line = f.read()
        lines = line.split('\n')
        for i in range(len(lines)):
            line_components = lines[i].split(':')
            dict_polarity[line_components[0]] = line_components[3]
    datasss = Message.objects.filter(Anime=post.id).values_list('content',flat=True)#values_list('引数',(引数が一個の場合flat=true))を追加．
    #ここにコードを書いてもいい
    so = []
    for i in datasss:
        so.append(i)
    list = []
    listt = []
    listtt = []
    for lo in so:
        t = Tokenizer()
        #形態素解析
        pol_val = 0
        for token in t.tokenize(lo):
            word = token.surface
            pos = token.part_of_speech.split(',')[0]
            if word in dict_polarity:
                pol_val = pol_val + float(dict_polarity[word])
        if pol_val > 0.3:#極性値の程度が0.3以下だった場合
           list.append(lo)
        elif pol_val < -0.3:
            listt.append(lo)
        else:
            listtt.append(lo)
   
    if request.method == 'POST':
        #下記はコメント記入フォーム
        if request.POST['mode'] == '_registerform_':
            obj = Message()#データベースのMessageモデルをインスタンス化
            form = MessageForm(request.POST,instance=obj)
            content = form.save(commit=False)#まだコメントは登録されてない、仮登録
            content.user = request.user#ユーザ取得
            content.Anime = post#コメントフォームのアニメが指定されていないので、ここで登録
            content.save()#アニメも指定し、ようやくここでMessageモデルを保存
            return redirect('message',num=num)
        
        if request.POST['mode'] == '_contentform_':
            #感想から探せる探索フォーム
            contentform = ContentForm(request.POST)
            str =request.POST['content']
            datas = Message.objects.filter(content__contains=str,Anime=post.id).order_by('id').reverse()
 

    else :
        #上記意外のフォーム入力が無い場合、これらの下記のものが実行される．
        contentform = ContentForm()
        datas = Message.objects.filter(Anime=post.id).order_by('id').reverse()
        
        

    
    pa = {
        #初期設定
        'data': data,
        'title': '感想',
        'id' : num,
        'form' : MessageForm(instance=post),
        'datas' : datas, 
        'contentform' : contentform,
        'list':list,
        'listt':listt,
        'listtt':listtt,
    }
    return render(request,'hello/message.html',pa)



@login_required(login_url='/admin/login/')
def medelete(request):
    datas = Message.objects.filter(user=request.user)

    pa = {
        'data' : '最高',
        'datas' : datas,
    }
    return render(request,'hello/medelete.html',pa)


@login_required(login_url='/admin/login/')
def delete(request,num):
    message = Message.objects.get(id=num)
    if (request.method == 'POST'):
        message.delete()
        return redirect(to='/hello/medelete')
    pa = {  
        'id' : num,
        'item' : message
    }
    return render(request,'hello/delete.html',pa)

@login_required(login_url='/admin/login/')
def gooddelete(request,num):
    anime = Good.objects.get(id=num)
    if (request.method == 'POST'):
        anime.delete()
        return redirect(to='/hello/favorite')
    pa = {
        'id' : num,
        'item' : anime
    }
    return render(request,'hello/gooddelete.html',pa)

@login_required(login_url='/admin/login/')
def update(request,num):
    obj = Anime.objects.get(id=num)
    if (request.method == 'POST'):
        anime = HelloForm(request.POST,instance=obj)
        anime.save()
        return redirect(to='/hello')
    pa = {
        'id' : num,
        'form' : HelloForm(instance=obj)
    }
    return render(request,'hello/delete.html',pa)

@login_required(login_url='/admin/login/')
def follow(request):
    #フォローした人を取得
    data = Friend.objects.filter(userid=request.user)

    pa = {
        'data':data,
    }
    return render(request,'hello/follow.html',pa)

@login_required(login_url='/admin/login/')
def favorite(request):
    #いいねしたアニメを取得
    data = Good.objects.filter(user=request.user)

    pa = {
        'data':data,
    }
    return render(request,'hello/favorite.html',pa)

@login_required(login_url='/admin/login/')
def whogood(request):
    datas = Friend.objects.filter(userid=request.user).values_list('follow')
    #？？_in=リストで「ある形がリストに含まれているか検索を行える．」
    data = Good.objects.filter(user__in=datas)

    if request.method =='POST':
        if request.POST['mode'] == '_userform_':
             #から探せる探索フォーム
             userform = UserForm(request.POST)
             str = request.POST['user']
             data = Good.objects.filter(user__username__contains=str).order_by('id').reverse()#ユーザが入力された文字を含むレコードを抽出

    else:
        #通常の画面
        userform = UserForm()
        data
        #コメントが寄せられたもの全て表示される．同じアニメが何件も表示される．

    pa = {
        'data':data,
        'userform':userform,
    }

    return render(request,'hello/whogood.html',pa)

@login_required(login_url='/admin/login/')
def finduser(request):
    if request.method =='POST':
        if request.POST['mode'] == '_userform_':
            form = FindUserForm(request.POST)
            str = request.POST.get('username')
            data = User.objects.filter(username__contains=str).order_by('id').reverse()

    else:
        form = FindUserForm()
        data = User.objects.all().order_by('id').reverse()
    
    pa = {
        'data':data,
        'form':FindUserForm
    }
    
    return render(request,'hello/finduser.html',pa)



@login_required(login_url='/admin/login/')
def add(request):
    #追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    #Userが本人だった場合
    if add_user == request.user:
        messages.info(request,"自分自身を追加することはできません")
        return redirect('follow')

    
    #add_userの数を調査
    frd_num = Friend.objects.filter(userid=request.user).filter(follow=add_user).count()

    (public_user) = get_public()

    #ゼロより大きければ既に登録してある．
    if frd_num > 0 :
        messages.info(request,add_user.username + 'は既に追加されています')
        return redirect('follow')

    frd = Friend()
    frd.userid = request.user
    frd.follow = add_user
    frd.save()
    #保存された時のメッセージを設定
    messages.success(request,add_user.username + 'を追加しました')
    return redirect(to='/hello/follow')

def get_public():
    public_user = User.objects.filter(username='public').first()
    return (public_user)

@login_required(login_url='/admin/login/')
def god(request,anime_id):
    #いいねするアニメを取得
    god_msg = Anime.objects.get(id=anime_id)
    #自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(user=request.user).filter(good=god_msg).count()
    #ゼロより大きければ登録済み
    if is_good > 0:
        messages.success(request,"過去にいいねをしています")
        return redirect('message',num=anime_id)
    
  
    god_msg.save()
    god = Good()
    god.user = request.user
    god.good = god_msg
    god.save()
    messages.success(request,"いいねしました")
    return redirect('message',num=anime_id)





#好きなアニメを共有できるようにする．いんすたの投稿を誰が良いねしたかを発見．
#また秘密のお気に入り機能も追加
#共有も可能

