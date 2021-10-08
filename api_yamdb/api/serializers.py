from rest_framework import serializers
#from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )
    
    
    class Meta:
        fields = '__all__'
        model = Review
        
    #def get_rate(self, obj):      
     #   return sum(obj.score)/len(obj.score)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
