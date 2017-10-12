
def testing(request):
    from django.http import JsonResponse
    from src.comments.api.serializers import CommentSerializer
    from src.likes.api.serializers import LikeSerializer

    profile_id = 1
    image_id = 9

    profile = Profile.objects.get(pk=profile_id)
    image = Image.objects.get(pk=image_id)

    # return JsonResponse(CommentSerializer(instance=profile.comment_set.all(), many=True).data, safe=False)
    return JsonResponse(LikeSerializer(instance=profile.like_set.all(), many=True).data, safe=False)