from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

class Anime(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    broadcaststart = models.CharField(max_length = 10) 
    broadcastfinish = models.CharField(max_length = 10)
    genre = models.CharField(verbose_name="genre",max_length=900)
    registerdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '< anime:id=' + str(self.id) + ',' + 'タイトル:' + self.title + ',' + '作者:' + self.author + ',' +\
        '放送開始日:' + self.broadcaststart  + ',' + '放送終了日:' + self.broadcastfinish + \
        ',' + 'ジャンル:' + self.genre + ',' + '登録日時:' + str(self.registerdate)

class Message(models.Model):
    Anime = models.ForeignKey(Anime,on_delete=models.CASCADE,verbose_name='対象アニメ')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='ユーザ')
    content = models.TextField(max_length = 1000,)#textに変換
    update = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '感想:' + self.content + '記入日:' + str(self.update)


class Friend(models.Model):
    userid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='フォロー',related_name="userowner")#誰がフォローを行ったか
    follow = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='ユーザ')#フォロー相手

class Good(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='ユーザ')#誰がいいねをしたか
    good = models.ForeignKey(Anime,on_delete=models.CASCADE,verbose_name='アニメ')#どの作品に対して良いねをしたか


class WhoGood(models.Model):
    friendgood = models.ForeignKey(Friend,on_delete=models.CASCADE,verbose_name='フォローした人')#どの作品に対して誰がアニメをいいねしたか特定するもの
    goodanime = models.ForeignKey(Anime,on_delete=models.CASCADE,verbose_name='アニメ')







