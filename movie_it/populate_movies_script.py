# 实现了从 movies.csv 文件中读取电影数据，并将其添加到 Django 项目中的数据库中，同时清空数据库中的已有数据
import os
import re

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")

django.setup()
from movie.models import Movie, Tags

Movie.objects.all().delete()
Tags.objects.all().delete()
opener = open('movies.csv', 'r',encoding='utf-8')
lines = opener.readlines()
for line in lines[1:]:
    id, name, image_link, country, years, director_description, leader, star, description, tags, flag = tuple(line.strip().split(','))
    res = re.match('\d*', star)
    int_d_rate_num = int(res[0]) if res else 0
    movie = Movie.objects.create(name=name, pic=name + '.png', country=country, years=years, leader=leader, d_rate_nums=int_d_rate_num, d_rate=star, intro=description, director=director_description, good='None')
    tags = [tag.strip() for tag in tags.split('/')]
    print(tags)
    for tag in tags:
        tag_obj, created = Tags.objects.get_or_create(name=tag)
        print('created', created)
        movie.tags.add(tag_obj.id)
