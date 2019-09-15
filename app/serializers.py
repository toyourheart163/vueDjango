from rest_framework import serializers

from .models import Blog


# Serializers define the API representation.
class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'