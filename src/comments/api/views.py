import ipdb
from django.http import JsonResponse
from pip import status_codes
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    get_object_or_404
from rest_framework.response import Response

from .serializers import CommentSerializer, CreateCommentSerializer, DetailedCommentSerializer
from .permissions import IsAdminOrOwnerOrReadOnly
from src.comments.models import Comment
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.albums.models import Album
from src.images.models import Image


class CreateGetCommentsAPI(ListAPIView, CreateAPIView):
    """

    """
    serializer_class = [CommentSerializer, CreateCommentSerializer]
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ("content__icontains",)
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        self.serializer_class = CommentSerializer

        image_id   = self.kwargs.get("image_id")
        if not image_id:
            return Response({"status": "fail"}, status=403)

        queryset_list = Comment.objects.filter(image__pk=image_id)
        return queryset_list

    def perform_create(self, serializer):
        if self.kwargs['profile_id']:
            profile = Profile.objects.get(user=self.request.user)
            serializer.save(owner=profile)

    def post(self, request, *args, **kwargs):
        serializer_class = CreateCommentSerializer

        owner_id = Profile.objects.get(user=request.user).id
        image_id = request.POST.get('image', self.kwargs.get("image_id"))
        content  = request.POST['content']

        if not owner_id:
            return JsonResponse({"status": "fail", "code": 406, "messages": ["No profile id provided."]})

        profile = Profile.objects.get(pk=owner_id)
        image   = Image.objects.get(pk=image_id)
        comment = Comment(content=content)
        comment.save()
        comment.owner.add(profile)
        comment.image.add(image)
        comment.save()
        image.save()
        return JsonResponse(serializer_class(instance=comment).data)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = DetailedCommentSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        profile_id = self.kwargs.get("profile_id")
        image_id   = self.kwargs.get("image_id")
        comment_id = self.kwargs.get("comment_id")

        if not (image_id and comment_id):
            return JsonResponse({"status": "fail", "code": 406})

        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404})

        comment = image.comment_set.get(pk=comment_id)
        if not comment:
            return JsonResponse({"status": "fail", "code": 404})

        return comment

    def put(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        if not comment_id:
            return JsonResponse({"status": "fail", "code": 406})

        comment = Comment.objects.get(pk=comment_id)

        if not comment:
            return JsonResponse({"status": "fail", "code": 404})

        comment.content = request.POST.get('content', comment.content)
        comment.save()

        return JsonResponse({"status": "success", "code": 200, "data": self.serializer_class(instance=comment).data,
                             "messages": ["Comment successfully updated!"]})


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
