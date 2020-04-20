from rest_framework import serializers
from .choices import (
    get_analyzer_choices,
    get_generator_dataset_choices,
    get_generator_language_choices,
    get_generator_location_choices
)


class EMBEDDIATextSerializer(serializers.Serializer):
    text = serializers.CharField()
    analyzers = serializers.MultipleChoiceField(choices=get_analyzer_choices(), required=False)

    def validate(self, data):
        analyzer = data["analyzers"]
        if not analyzer:
            data["analyzers"] = [a[0] for a in get_analyzer_choices()]
        return data


class EMBEDDIAGenerateTextSerializer(serializers.Serializer):
    dataset = serializers.ChoiceField(choices=get_generator_dataset_choices(), required=False)
    location = serializers.ChoiceField(choices=get_generator_location_choices(), required=False)
    language = serializers.ChoiceField(choices=get_generator_language_choices(), required=False)
