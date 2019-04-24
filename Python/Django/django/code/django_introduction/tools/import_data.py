#!/usr/bin/python
# -*-encoding=utf8 -*-


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_introduction.settings')
django.setup()

from blog.models import Article

data_path = '../data/article'


def main():
    content_list = []
    files = os.listdir(data_path)
    for name in files:
        f = os.path.join(data_path, name)
        with open(f, 'r', encoding='utf-8') as f:
            content = f.read()
            item = (name[:-4], content[:100], content)
            content_list.append(item)
    # Article.objects.all().delete()
    for item in content_list:
        print('saving article: %s' % item[0])
        article = Article()
        article.title = item[0]
        article.brief_content = item[1]
        article.content = item[2]
        article.save()


if __name__ == '__main__':
    main()
