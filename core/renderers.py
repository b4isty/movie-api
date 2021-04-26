from rest_framework.renderers import JSONRenderer


class MovieListJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data.get('results'):

            result = data.pop('results')
            data['data'] = result
        return super(MovieListJSONRenderer, self).render(data, accepted_media_type, renderer_context)


class CollectionListRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        print(type(data))
        if data.get('results'):
            result = data.pop('results')
            data = dict()
            favorite_genres = result.pop('favorite_genres')
            data['favorite_genres'] = favorite_genres
            data['collections'] = result
        return super(CollectionListRenderer, self).render(data, accepted_media_type, renderer_context)


