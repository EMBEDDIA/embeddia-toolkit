from rest_framework import serializers
from embeddia_toolkit.settings import ARTICLE_ANALYZERS, COMMENT_ANALYZERS


ARTICLE_ANALYZERS = [(a, a) for a in ARTICLE_ANALYZERS]
COMMENT_ANALYZERS = [(a, a) for a in COMMENT_ANALYZERS]


class EMBEDDIAArticleSerializer(serializers.Serializer):
    text = serializers.CharField()
    analyzers = serializers.MultipleChoiceField(
        choices=ARTICLE_ANALYZERS,
        default=[]
    )

class EMBEDDIACommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    analyzers = serializers.MultipleChoiceField(
        choices=COMMENT_ANALYZERS,
        default=[]
    )
