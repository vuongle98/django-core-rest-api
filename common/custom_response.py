from rest_framework.renderers import JSONRenderer
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

class CustomResponse(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None, **kwargs):

        response_structure = {
            "status": "success",
            "data": None,
            "code": None,
            "message": None
        }

        response = renderer_context.get("response")

        if 200 <= response.status_code < 300:
            response_structure["data"] = data
            response_structure["code"] = response.status_code
            response_structure["message"] = "success"
        else:
            response_structure["status"] = "error"
            response_structure["message"] = response.reason_phrase
            response_structure["code"] = response.status_code

        return super(CustomResponse, self).render(response_structure, accepted_media_type, renderer_context, **kwargs)


class CustomCamelCaseResponse(CamelCaseJSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None, **kwargs):

        response_structure = {
            "status": "success",
            "data": None,
            "code": None,
            "message": None
        }

        response = renderer_context.get("response")

        if 200 <= response.status_code < 300:
            response_structure["data"] = data
            response_structure["code"] = response.status_code
            response_structure["message"] = "success"
        else:
            response_structure["status"] = "error"
            response_structure["message"] = response.reason_phrase
            response_structure["code"] = response.status_code

        return super(CustomCamelCaseResponse, self).render(response_structure, accepted_media_type, renderer_context, **kwargs)