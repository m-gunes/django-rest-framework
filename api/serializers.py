from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post:detail', lookup_field='slug')

    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'draft', 'image', 'created_at', 'updated_at', 'slug']
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'draft', 'image']
    
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('title', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.save()
    #     return instance

    # def validate_title(self, value):
    #     if value == 'sex':
    #         raise serializers.ValidationError('Agir ol kardes')
    #     return value

    # def validate(self, attrs):
    #     print(attrs['title'])
    #     if attrs['title'] == 'sex':
    #         raise serializers.ValidationError('Agir ol kardes')
    #     return super().validate(attrs)
        
    

