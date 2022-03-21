from flask_restx import Resource as RESTXResource


class Resource(RESTXResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init", self.__class__.__name__)
