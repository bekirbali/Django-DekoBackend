from rest_framework import serializers
from .models import Product, ProductImage, ProductDocument

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'description']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductDocumentSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = ProductDocument
        fields = ['id', 'title', 'document', 'description']

    def get_document(self, obj):
        request = self.context.get('request')
        if obj.document and hasattr(obj.document, 'url'):
            return request.build_absolute_uri(obj.document.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    additional_images = ProductImageSerializer(many=True, required=False)
    documents = ProductDocumentSerializer(many=True, required=False)

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
        images_data = validated_data.pop('additional_images', [])
        documents_data = validated_data.pop('documents', [])
        product = Product.objects.create(**validated_data)
        for image in images_data:
            ProductImage.objects.create(product=product, **image)
        for document in documents_data:
            ProductDocument.objects.create(product=product, **document)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('additional_images', [])
        documents_data = validated_data.pop('documents', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update images
        if images_data:
            instance.additional_images.all().delete()
            for image in images_data:
                ProductImage.objects.create(product=instance, **image)
        # Update documents
        if documents_data:
            instance.documents.all().delete()
            for document in documents_data:
                ProductDocument.objects.create(product=instance, **document)
        return instance 