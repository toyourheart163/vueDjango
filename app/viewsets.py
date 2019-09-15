from rest_framework import viewsets

from .models import Blog
from .serializers import BlogSerializer


# ViewSets define the view behavior.
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer