from rest_framework import serializers

ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg', 'bmp', 'gif')


class ImageSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_extension(image):
        extension = image.rsplit('.')[-1]
        if extension.lower() not in ALLOWED_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(
                {'status': f'Invalid uploaded image type: {image}'}
            )
