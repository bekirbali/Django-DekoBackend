from rest_framework import serializers
from .models import Product, ProductDetail, ProductImage

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        exclude = ['product']

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        exclude = ['product']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    details = ProductDetailSerializer(many=True, required=False)
    additional_images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        exclude = ['updated_at']
        read_only_fields = ['id', 'created_at']

    def get_main_image(self, obj):
        request = self.context.get('request')
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return request.build_absolute_uri(obj.main_image.url)
        return None

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        images_data = validated_data.pop('additional_images', [])
        product = Product.objects.create(**validated_data)
        for detail in details_data:
            ProductDetail.objects.create(product=product, **detail)
        for image in images_data:
            ProductImage.objects.create(product=product, **image)
        return product

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        images_data = validated_data.pop('additional_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update details
        if details_data:
            instance.details.all().delete()
            for detail in details_data:
                ProductDetail.objects.create(product=instance, **detail)
        # Update images
        if images_data:
            instance.additional_images.all().delete()
            for image in images_data:
                ProductImage.objects.create(product=instance, **image)
        return instance 