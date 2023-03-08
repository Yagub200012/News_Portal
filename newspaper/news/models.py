from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.



class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_rating = models.IntegerField(default=1)

    def update_raiting(self):
        a1, b1, c1 = 0, 0, 0
        for x in list(Post.objects.filter(author_id=self).values('post_rating')):
            a1 += x['post_rating']
        for x in list(Comment.objects.filter(user_id=self.user_id).values('comm_rating')):
            b1 += x['comm_rating']
        for x in list(Post.objects.filter(author_id=self)):
            for y in list(Comment.objects.filter(post_id=x).values('comm_rating')):
                c1 += y['comm_rating']
        self.auth_rating = 3 * a1 + b1 + c1
        self.save()


policy = 'PL'
crime = 'CR'
technologies = 'TC'
sport = 'SP'
music = 'MS'
science = 'SC'
economy = 'EC'

CATEGORIES = [(policy, 'Политика'),
              (crime, 'Криминал'),
              (technologies, 'Технологии'),
              (sport, 'Спорт'),
              (music, 'Музыка'),
              (science, 'Наука'),
              (economy, 'Экономика')]


class Category(models.Model):
    categ_name = models.CharField(max_length=2, choices=CATEGORIES, null=False)

    def __str__(self):
        return self.categ_name.title()


article = 'AR'
news = 'NW'

STATIA_NOVOST = [(article, 'статья'),
                 (news, 'новость')]


class Post(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    cathegory_id = models.ManyToManyField(Category, through='PostCategory')
    post_format = models.TextField(max_length=2, choices=STATIA_NOVOST, null=False)
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(null=False, max_length=80)
    post_text = models.TextField(null=False)
    post_rating = models.IntegerField(default=1)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating <= 1:
            pass
        else:
            self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:124] + '...'

    def __str__(self):
        return f'{self.post_title}: {self.post_text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    cathegory_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comm_text = models.TextField(null=False)
    comm_datetime = models.DateTimeField(auto_now_add=True)
    comm_rating = models.IntegerField(default=1)

    def like(self):
        self.comm_rating += 1
        self.save()

    def dislike(self):
        if self.comm_rating <= 1:
            pass
        else:
            self.comm_rating -= 1
        self.save()

class UserCategory(models.Model):
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
