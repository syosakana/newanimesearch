from django import forms
from .models import Anime,Message,Friend,Good,WhoGood
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class HelloForm(forms.Form):
    data = [
             ('SF/ファンタジー','SF/ファンタジー'),
             ('ロボット・メカ','ロボット・メカ'),
             ('アクション・バトル','アクション・バトル'),
             ('コメディ・ギャグ','コメディ・ギャグ'),
             ('恋愛・ラブコメ','恋愛・ラブコメ'),
             ('日常・ほのぼの','日常・ほのぼの'),
             ('スポーツ・熱血','スポーツ・熱血'),
             ('ホラー・サスペンス','ホラー・サスペンス'),
             ('推理・探偵','推理・探偵'),
             ('歴史・戦記','歴史・戦記'),
             ('戦争','戦争'),
             ('ドラマ','ドラマ'),
             ('青春・学園もの','青春・学園もの'),
             ('子供向け','子供向け'),
             ('家族向け','家族向け'),
             ('短編アニメ','短編アニメ'),
             ('異世界・転生','異世界・転生'),
    ]
    title = forms.CharField(label='タイトル')
    author = forms.CharField(label='作者')
    broadcaststart = forms.DateField(label='放送開始日')
    broadcastfinish = forms.DateField(label='放送終了日',) #(default='放送中')
    genre = forms.ChoiceField(label='ジャンル',choices = data)
    

class MessageForm(forms.ModelForm):
    #データベースから参照にしている
    #model.pyで登録した型（整数型や、文字列）などの指定を引用している．
    class Meta:
        model = Message
        exclude = ('Anime',)
        fields = ('content',)
        labels = {#どのような表示にするか
            'content' : '感想投稿',

        }
    
class FindForm(forms.Form):
    find = forms.CharField(label='タイトル',required=False)


class GenreForm(forms.Form):
    data = [
             ('SF/ファンタジー','SF/ファンタジー'),
             ('ロボット・メカ','ロボット・メカ'),
             ('アクション・バトル','アクション・バトル'),
             ('コメディ・ギャグ','コメディ・ギャグ'),
             ('恋愛・ラブコメ','恋愛・ラブコメ'),
             ('日常・ほのぼの','日常・ほのぼの'),
             ('スポーツ・熱血','スポーツ・熱血'),
             ('ホラー・サスペンス','ホラー・サスペンス'),
             ('推理・探偵','推理・探偵'),
             ('歴史・戦記','歴史・戦記'),
             ('戦争','戦争'),
             ('ドラマ','ドラマ'),
             ('青春・学園もの','青春・学園もの'),
             ('子供向け','子供向け'),
             ('家族向け','家族向け'),
             ('短編アニメ','短編アニメ'),
             ('異世界・転生','異世界・転生'),
    ]
    genre = forms.ChoiceField(label='ジャンル',choices = data,required=False)

class AuthorForm(forms.Form):
    author = forms.CharField(label=' 作者',required=False)

class ContentForm(forms.Form):
    content = forms.CharField(label='感想',required=False)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['userid','follow']

class FindUserForm(forms.Form):
    username = forms.CharField(label='ユーザ',required=False)


class UserForm(forms.Form):
    user = forms.CharField(label='ユーザ',required=False)

class FriendForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super(FriendForm,self).__init__(*args,**kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user,item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )
    
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['user','good']


