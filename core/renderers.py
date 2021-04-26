import json

from rest_framework.renderers import JSONRenderer


class MovieListJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # sometime it's coming as json string, couldn't figure out
        # so it's a quick fix
        if not isinstance(data, dict):
            data = json.loads(data)

        if data.get('results'):
            result = data.pop('results')
            data['data'] = result
        return super(MovieListJSONRenderer, self).render(data, accepted_media_type, renderer_context)


class RequestCounterJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data.get("results"):
            result = data.pop('results')[0]
            data["requests"] = result["count"]
        return super(RequestCounterJSONRenderer, self).render(data, accepted_media_type, renderer_context)

