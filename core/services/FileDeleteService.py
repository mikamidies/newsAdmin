from django.core.files.storage import default_storage
from django.http.request import HttpRequest


class FileDeleteService:
    keys = list()

    def __init__(self, keys) -> None:
        self.keys = keys

    # pre delete ctg images
    def predelete_image(self, request: HttpRequest, id = ""):
        for key in self.keys:
            files = request.session.get(key)

            if not files: continue

            for it in list(files):
                if it['id'] == str(id) and default_storage.exists(it['name']):
                    default_storage.delete(it['name'])

                    request.session[key].remove(it)
                    request.session.modified = True


    # clean session
    def clean_session(self, request, id = ""):
        for key in self.keys:
            sess_images = request.session.get(key)

            if not sess_images: continue

            for item in list(sess_images):
                if str(item['id']) == str(id):
                    request.session.get(key).remove(item)
                    request.session.modified = True
