import ipdb
from django.http import JsonResponse
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    get_object_or_404
from rest_framework.response import Response

from .serializers import CommentSerializer, CreateCommentSerializer, DetailedCommentSerializer
from src.comments.models import Comment
from src.profiles.models import Profile
from src.gallery.helpers import log
from src.albums.models import Album
from src.images.models import Image


class GetCommentsAPI(ListAPIView):
    """

    """
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        image_id = self.kwargs.get("image_id")
        if not profile_id:
            if image_id:
                return Comment.objects.filter(image__pk=image_id)
            return Response({"status": "fail"}, status=403)

        profile = Profile.objects.get(pk=profile_id)

        album_id = self.kwargs.get("album_id")
        if not album_id:
            return Response({"status": "fail"}, status=403)
        # album = Album.objects.get(pk=album_id, profile__pk=profile_id)
        album = profile.albums.get(pk=album_id)

        if not album:
            return Response({"status": "fail"}, status=404)

        if not image_id:
            return Response({"status": "fail"}, status=403)
        image = Image.objects.get(pk=image_id, album_id=album_id)

        queryset_list = image.comment_set.all()
        return queryset_list


class CreateCommentAPI(CreateAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.kwargs['profile_id']:
            profile = Profile.objects.get(user=self.request.user)
            serializer.save(owner=profile)

    def post(self, request, *args, **kwargs):
        # ipdb.set_trace()
        owner_id = Profile.objects.get(user=request.user).id
        image_id = request.POST.get('image', self.kwargs.get("image_id"))
        content = request.POST['content']
        if not owner_id:
            return JsonResponse({"status": "fail", "code": 501, "messages": ["No profile id provided."]})

        profile = Profile.objects.get(pk=owner_id)
        image = Image.objects.get(pk=image_id)
        comment = Comment(content=content)
        comment.save()
        comment.owner.add(profile)
        comment.image.add(image)
        comment.save()
        image.save()
        return JsonResponse(self.serializer_class(instance=comment).data)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Comment.objects.all()
    serializer_class = DetailedCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        image_id = self.kwargs.get("image_id")
        comment_id = self.kwargs.get("comment_id")

        if not profile_id:
            if image_id and comment_id:
                # return Image.objects.get(pk=image_id).comments.get(pk=comment_id)
                return Comment.objects.get(pk=comment_id)
                # return get_object_or_404(queryset=Comment.objects.all(), pk=comment_id, image__pk=image_id)
            return JsonResponse({"status": "fail", "code": 406})

        profile = Profile.objects.get(pk=profile_id)
        if not profile:
            return JsonResponse({"status": "fail", "code": 404})

        album_id = self.kwargs.get("album_id")
        album = Album.objects.get(pk=album_id)
        if not album:
            return JsonResponse({"status": "fail", "code": 404})

        image = Image.objects.get(pk=image_id)
        if not image:
            return JsonResponse({"status": "fail", "code": 404})

        if not comment_id:
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
