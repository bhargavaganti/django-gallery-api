from django.http import *
from django.http import JsonResponse
from src.comments.api.serializers import CommentSerializer
from src.likes.api.serializers import LikeSerializer
from src.profiles.models import Profile
from src.albums.models import Album
from src.images.models import Image
from src.likes.models import Like
from src.comments.models import Comment
from src.tags.models import Tag

def testing(request):
    """
    Функција коришћена за разна тестирања;
    Позива се као /api/testing
    :param request:
    :return:
    """


    profile_id = 8
    # image_id = 9

    profile = Profile.objects.get(pk=profile_id)
    image = Image.objects.get(pk=image_id)

    return JsonResponse(CommentSerializer(instance=profile.comment_set.all(), many=True).data, safe=False)
    # return JsonResponse({"data":LikeSerializer(instance=profile.like_set.all(), many=True).data}, safe=False)


