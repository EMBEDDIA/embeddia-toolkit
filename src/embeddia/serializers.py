from rest_framework import serializers
from .choices import get_analyzer_choices


class EMBEDDIATextSerializer(serializers.Serializer):
    text = serializers.CharField()
    analyzers = serializers.MultipleChoiceField(choices=get_analyzer_choices(), required=False)

    def validate(self, data):
        analyzer = data["analyzers"]
        if not analyzer:
            data["analyzers"] = [a[0] for a in get_analyzer_choices()]
        return data
