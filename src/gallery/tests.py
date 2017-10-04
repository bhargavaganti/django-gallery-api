# from django.test import TestCase
# from random import random, randint, randrange
#
# from django.contrib.auth.models import User
# from src.profiles.models import Profile
# from src.albums.models import Album
# from src.images.models import Image
# from src.tags.models import Tag
# from src.likes.models import Like
# from src.comments.models import Comment
#
# # креирање корисника и профила
# for i in range(1, 4):
#     user = User.objects.create(
#         username="Test" + str(i),
#         email="test" + str(i) + "@example.com",
#         is_active=True,
#         is_superuser=True if randrange(1, 2) == 2 else False
#     )
#     user.set_password("test" + str(i))
#     user.save()
#
#     Profile.objects.create(
#         owner=user,
#         profile_picture=None
#     ).save()
#
# # креирање албума
# for i in range(1, 5):
#     album = Album.objects.create(
#         name="test album " + str(i),
#         owner=Profile.objects.get(pk=randrange(1, 4)),
#         description="some description " + str(i),
#         is_public=True if randrange(1, 4) % 2 == 0 else False
#     )
#     album.save()
#
# # креирање слика
# for i in range(1, 20):
#     image = Image.objects.create(
#         name="test album " + str(i),
#         album=Album.objects.get(pk=randrange(1, 5)),
#         description="some description " + str(i),
#         is_public=True if randrange(1, 5) % 2 == 0 else False
#     )
#     image.save()
#
# # креирање тагова
# for i in range(1, 20):
#     tag = Tag.objects.create(
#         name="Tag " + str(i),
#     )
#     tag.save()
#
# # креирање лајкова, коментара и тагова
# for i in range(1, 30):
#     like = Like.objects.create(
#         owner=Profile.objects.get(pk=randrange(1, 4)),
#         image=Image.objects.get(pk=randrange(1, 20))
#     )
#     like.save()
#
#     comment = Comment.objects.create(
#         owner=Profile.objects.get(pk=randrange(1, 4)),
#         image=Image.objects.get(pk=randrange(1, 20))
#     )
#     comment.save()
#
#     image = Image.objects.get(pk=randrange(1, 20))
#     tag = Tag.objects.get(pk=randrange(1, 20))
#     image.tags.add(tag)
#     image.save()


import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openroad.settings')

import django
# Import settings
django.setup()

from random import randint, choice
from django.contrib.auth.models import User
from src.profiles.models import Profile
from src.albums.models import Album
from src.images.models import Image
from src.tags.models import Tag
from src.likes.models import Like
from src.comments.models import Comment
from faker import Faker

fakegen = Faker()

my_word_list = [
'danish','cheesecake','sugar',
'Lollipop','wafer','Gummies',
'sesame','Jelly','beans',
'pie','bar','Ice','oat',
'group', 'octopus', 'noble',
'crocodile', 'gravel', 'excellent', 'destiny',
'bleeding', 'phenomena', 'downward'
]



def populate(N=5):
    for entry in range(N):
        # Create Fake Data for entry
        fake_company = fakegen.company()
        fake_name = fakegen.name().split()
        fake_poc = fake_name[0] + ' ' + fake_name[1]
        fake_contact = randint(1111111111, 9999999999)
        fake_street = fakegen.address().split('\n')
        fake_city = fake_street[1].split(',')
        fake_state = fake_city[1].split()
        fake_zip = fake_state[1].split('-')
        fake_notes = fakegen.text()
        fname = fakegen.name()
        lname = fakegen.name()
        username = fakegen.email().split("@")[0]
        email = fakegen.email()
        url = fakegen.url()

        count = 0
        tag_count = randint(1, 4)
        tags = []
        while count <= tag_count:
            tags.append(choice(my_word_list))
            count += 1

        tags = ",".join(str(x) for x in tags)

        user = User.objects.get_or_create(
            first_name=fname,
            last_name=lname,
            username=username,
            email=email
        )
        user.set_password("password123")
        user.save()

        profile = Profile.objects.get_or_create(
            owner=user,
            profile_pictore=url
        )
        profile.save()

if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    populate(1)
    print('Populating Complete')