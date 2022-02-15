from api import ma
from api.models.tag import TagModel


# Сериализация ответа(response)
class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        fields = ("id", "name",)

    _links = ma.Hyperlinks({
        'self': ma.URLFor('tokensource', values=dict(token_id="<id>")),
        'collection': ma.URLFor('tokenlistresource')
    })


# Десериализация запроса(request)
class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()