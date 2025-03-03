import graphene
from graphene_django import DjangoObjectType

from users.schema import UserType
from .models import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()


class CreatePost(graphene.Mutation):
    id = graphene.Int()
    text = graphene.String()
    author = graphene.Field(UserType)

    class Arguments:
        text = graphene.String()

    def mutate(self, info, text):
        user = info.context.user or None

        post = Post(
            text=text,
            author=user
        )
        post.save()

        return CreatePost(
            id=post.id,
            text=post.text,
            author=post.author
        )


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
