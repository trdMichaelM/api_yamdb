import random

from django.contrib.auth import get_user_model
from django.db.models import Avg

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Title

User = get_user_model()


def confirmation_code_generator():
    upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_case = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    base = upper_case + lower_case + numbers
    length = 16
    confirmation_code = ''.join(random.sample(base, length))
    return confirmation_code


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено.'
            )
        return data

    def is_valid(self):
        """
        Логики переопределения метода is_valid заключается в том что,
        по заданию юзера можно создать через админку, и если мы потом пытаемся
        запросить код подтверждения, мы получает ошибку от модели, что поля
        с указанными username и email уже существуют, переопределив метод,
        проверяем на наличие юзера и если он существует, возвращаем True.
        А в методе create используем get_or_create().
        """
        if User.objects.filter(**self.initial_data).exists():
            self._validated_data = self.initial_data
            self._errors = {}
            return True
        return super().is_valid()

    def create(self, validated_data):
        user, status = User.objects.get_or_create(**validated_data)
        user.confirmation_code = confirmation_code_generator()
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate(self, data):
        user = self.context['request'].user
        method = self.context['request'].method
        if method == 'PATCH' and user.role == 'user' and 'role' in data:
            data.pop('role')
        return data

#class TitleSerializer(serializers.ModelSerializer):
    
#    rating = serializers.SerializerMethodField(source='reviews',read_only=True)
    
#    class Meta:
#        fields = ('id', 'name', 'rating')
#        model = Title

#    def get_rating(self,obj):
#        rate = obj.reviews.aggregate(average_score=Avg('score'))
#        return rate.get('average_score')
        

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    
    title = serializers.StringRelatedField(
        read_only=True,
    )
    
    class Meta:
        fields = ('id', 'title', 'author',  'text', 'score','pub_date')
        model = Review
        
    
    def validate(self, data):
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        author = self.context['request'].user
        if (self.context['request'].method == "POST"
                and Review.objects.filter(
                    title=title,
                    author=author
                ).exists()):
            raise serializers.ValidationError('один автор - одно произведение-одно ревью!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'pub_date', 'text')
        model = Comment


  
            
   


 
