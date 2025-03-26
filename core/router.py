from django.http.request import HttpRequest
from django.views.decorators.http import require_GET, require_POST
from django.urls import path


class BaseRouter:
    url: str
    GET_urls: dict
    POST_urls: dict
    COMBINED_urls: dict

    def __init__(self, url: str) -> None:
        self.POST_urls = dict()
        self.GET_urls = dict()
        self.COMBINED_urls = dict()
        self.url = url

    def require_GET_and_POST_controller(self, GET_controller, POST_controller):
        def controller(request: HttpRequest, *args, **kwargs):
            if request.method == "GET":
                return require_GET(GET_controller)(request, *args, **kwargs)

            elif request.method == "POST":
                return require_POST(POST_controller)(request, *args, **kwargs)

        return controller

    def GET_request(self, url: str, name: str):
        def register(fn):
            key_url = self.url + url

            if key_url in self.POST_urls:
                post_controller = self.POST_urls.get(key_url, {})

                controller = self.require_GET_and_POST_controller(fn, post_controller["controller"])

                self.COMBINED_urls[key_url] = {
                    "controller": controller,
                    "name": name
                }

                del self.POST_urls[key_url]

            elif key_url not in self.GET_urls:
                controller = require_GET(fn)
                self.GET_urls[key_url] = {
                    "controller": controller,
                    "name": name
                }

            else:
                raise Exception(f"Url {key_url} alread registered with GET method")

            return fn

        return register

    def POST_request(self, url: str, name: str):
        def register(fn):
            key_url = self.url + url

            if key_url in self.GET_urls:
                get_controller = self.GET_urls.get(key_url, {})

                controller = self.require_GET_and_POST_controller(get_controller["controller"], fn)

                self.COMBINED_urls[key_url] = {
                    "controller": controller,
                    "name": name
                }

                del self.GET_urls[key_url]

            elif key_url not in self.POST_urls:
                controller = require_POST(fn)
                self.POST_urls[key_url] = {
                    "controller": controller,
                    "name": name
                }
            else:
                raise Exception(f"Url {key_url} alread registered with POST method")

            return fn

        return register

    @property
    def paths(self):
        paths: list = list()

        for url, data in self.COMBINED_urls.items():
            paths.append(
                path(f"{url}", data["controller"], name=data["name"])
            )

        for url, data in self.GET_urls.items():
            paths.append(
                path(f"{url}", data["controller"], name=data["name"])
            )


        for url, data in self.POST_urls.items():
            paths.append(
                path(f"{url}", data["controller"], name=data["name"])
            )

        return paths
