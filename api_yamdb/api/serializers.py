from rest_framework import serializers

from reviews.models import Comment, Review, Title
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg,Count
class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )
    
    
    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title_id']
            )]
        

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment


  
            
   

class TitleSerializer(serializers.ModelSerializer):
    
    rating = serializers.SerializerMethodField() 
    class Meta:
        fields = ('name',  'rating')
        model = Title
    def get_rating(self,obj):
           
        return obj.rating.aggregate(average_score=Avg('score'))
        
 