import json

from src.images.models import Image
from src.images.api.serializers import ImageSerializer

obj = Image.objects.filter(album__pk=1)

print(obj)

data = ImageSerializer(obj, many=True)
print(json.dumps(data.data))