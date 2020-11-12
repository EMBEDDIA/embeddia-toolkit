from rest_framework import serializers
from embeddia_toolkit.settings import EMBEDDIA_ARTICLE_ANALYZER, EMBEDDIA_COMMENT_ANALYZER


ARTICLE_ANALYZERS = [(a, a) for a in EMBEDDIA_ARTICLE_ANALYZER.analyzers.keys()]
COMMENT_ANALYZERS = [(a, a) for a in EMBEDDIA_COMMENT_ANALYZER.analyzers.keys()]


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
