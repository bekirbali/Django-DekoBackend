from rest_framework import serializers
from .models import News, NewsDetail, NewsImage

class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsDetail
        fields = ['title', 'context']

class NewsImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsImage
        fields = ['image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class NewsSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    details = NewsDetailSerializer(many=True, read_only=True)
    additional_images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ['id', 'main_title', 'sub_title', 'main_context', 'main_image', 'created_at', 'updated_at', 'details', 'additional_images']

    def get_main_image(self, obj):
        request = self.context.get('request')
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return request.build_absolute_uri(obj.main_image.url)
        return None 