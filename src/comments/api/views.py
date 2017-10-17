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
    Класа која се користи за креирање коментара и за добављање листе
    свих коментара слике репрезентованих у JSON формату
    """

    # класе за серијализацују које ће се применити
    serializer_class = CommentSerializer

    # укључивање могућности филтрирања
    filter_backends = [SearchFilter]  # ово мора бити низ!

    # поља по којима ће претрага бити вршена
    search_fields = ("content__icontains",)

    # класе права приступа
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        """
        Mетода помоћу које се добављају сви подаци
        :param args:
        :param kwargs: image_id
        :return: QuerySet
        """

        self.serializer_class = CommentSerializer # експлицитно назначавање која се серијализација користи

        image_id = self.kwargs.get("image_id")
        if not image_id:
            return JsonResponse(
                {"status": "fail", "code": 406, "data": None, "messages": ["Error: No image id provided!"]})

        queryset_list = Comment.objects.filter(image__pk=image_id)
        return queryset_list


    def post(self, request, *args, **kwargs):
        """
        Mетода помоћу које се врши креирање
        :param request:
        :param args:
        :param kwargs: image_id
        :return: Album|Http404
        """

        # ipdb.set_trace()
        self.serializer_class = CreateCommentSerializer # експлицитно навођење која ће се класа за серијализацију користити
        self.permission_classes = [IsAuthenticated] # експлицитно навођење која ће се класа за права приступа користити

        owner_id = Profile.objects.get(user=request.user).id
        image_id = request.POST.get('image', self.kwargs.get("image_id"))
        content  = request.POST['content']

        if not owner_id:
            return JsonResponse({"status": "fail", "code": 406, "data":None, "messages": ["No profile id provided."]})

        profile = get_object_or_404(Profile, pk=owner_id)
        image   = get_object_or_404(Image, pk=image_id)
        comment = Comment(content=content)
        comment.save()
        # асоцијација са профилом
        comment.owner.add(profile)
        # асоцијација са сликом
        comment.image.add(image)
        comment.save()
        image.save()
        return JsonResponse({"status": "success", "code": 200, "data":self.serializer_class(instance=comment).data,
                             "messages": ["Comment successfully created!"]})



class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """
    Класа која се користи за приказ, ажурирање и брисање инстанце класе Коментар;
    Репрезентује податке у JSON формату
    """
    queryset           = Comment.objects.all()
    serializer_class   = DetailedCommentSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    def get_object(self):
        """
        Mетода која се користи за добијање појединачног објекта
        Окида се на HTTP GET методу
        :return: Comment | Http404
        """
        profile_id = self.kwargs.get("profile_id")
        image_id   = self.kwargs.get("image_id")
        comment_id = self.kwargs.get("comment_id")

        if not (image_id and comment_id):
            return JsonResponse({"status": "fail", "code": 406, "data": None,
                             "messages": ["Error: No image or comment id provided"]})

        image = get_object_or_404(Image, pk=image_id)

        # приступање сету коментара који су у асоцијацији са сликом
        comment = get_object_or_404(queryset=image.comment_set.all(),pk=comment_id)
        return comment

    def put(self, request, *args, **kwargs):
        """
        Метода која се користи за ажурирање објекта
        Окида се на HTTP PUT методу
        :param request: content
        :param args:
        :param kwargs: image_id, comment_id
        :return: Comment | Http404
        """
        comment_id = self.kwargs.get("comment_id")
        if not comment_id:
            return JsonResponse({"status": "fail", "code": 406, "data": None,
                                 "messages": ["Error: No comment id provided"]})

        comment = get_object_or_404(Comment, pk=comment_id)
        comment.content = request.POST.get('content', comment.content)
        comment.save()
        return comment


    def delete(self, request, *args, **kwargs):
        """
        Meтода која се користи за брисање инстанце
        Окида се на HTTP DELETE методу
        :param request: user
        :param args:
        :param kwargs: comment_id
        :return: JsonResponse
        """

        return self.destroy(request, *args, **kwargs)
