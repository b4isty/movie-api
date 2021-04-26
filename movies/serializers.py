from django.db.models import Count
from rest_framework import serializers

from movies.models import Collection, Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source='collection_uuid', required=False)
    # movies = serializers.SerializerMethodField('get_movies_titles')
    movies = MovieSerializer(many=True, write_only=True)
    favorite_genres = serializers.SerializerMethodField('get_favorite_genres')

    class Meta:
        model = Collection
        exclude = ('id', 'collection_uuid', 'user')

        extra_kwargs = {
            "movies": {"required": True, 'write_only': True},
        }

    def get_favorite_genres(self, obj):
        """
        Return top3 movie genres by annotating
        """
        top_three_genres = (
            Collection.objects.filter(user=obj.user)
                .values("movies__genres")
                .annotate(total=Count("movies__genres"))
                .values_list("movies__genres", flat=True)
                .order_by("-total")[:3]
        )
        return top_three_genres

    def create(self, validated_data):
        """
        Overriding create cause drf model serializer do not supports nested write
        """
        movies = validated_data.pop('movies', {})
        collection = super(CollectionSerializer, self).create(validated_data)
        if movies:
            movie_obj_list = list()
            for movie in movies:
                movie_obj_list.append(Movie(**movie))
            movie_objs = Movie.objects.bulk_create(movie_obj_list)
            collection.movies.add(*movie_objs)
        return collection

    def to_representation(self, instance):
        representation = super(CollectionSerializer, self).to_representation(instance)
        request = self.context['request']
        if request.method == 'POST':
            return {'collection_uuid': representation['uuid']}
        return representation


class CollectionUpdateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies', ]
        extra_kwargs = {
            "movies": {"required": False},
            "title": {"required": False},
            "description": {"required": False},
        }

    def update(self, instance, validated_data):
        movies = self.validated_data.pop('movies', None)
        instance.title = validated_data.pop('title', instance.title)
        instance.description = validated_data.pop('description', instance.description)
        instance.save()
        if movies:
            movie_obj_list = list()
            for movie in movies:
                movie_obj_list.append(Movie(**movie))
            movie_objs = Movie.objects.bulk_create(movie_obj_list)
            instance.movies.add(*movie_objs)
        return instance





