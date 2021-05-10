from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE,
                                  unique=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_author = Post.objects.filter(author=self.id)
        post_rating = sum([n.post_rating * 3 for n in post_author])
        comment_rating = sum([n.comment_rating for n in Comment.objects.filter(user=self.id)])
        post_comment_rating = sum([n.comment_rating for n in Comment.objects.filter(post__in = post_author)])
        self.author_rating = post_rating + comment_rating + post_comment_rating
        print(self.author_rating)
        self.save()

    def __str__(self):
        return self.author.username


class Category(models.Model):
    name_category = models.CharField(max_length=255,
                                     unique=True)

    def __str__(self):
        return self.name_category


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    news = 'NW'
    article = 'AR'

    CHOICES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    type = models.CharField(max_length=2,
                            choices=CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=1000)
    text = models.TextField(null=True)
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    @staticmethod
    def preview():
        return Post.text[:124] + '...'

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return str(self.user.username) + ' - ' + str(self.id)
