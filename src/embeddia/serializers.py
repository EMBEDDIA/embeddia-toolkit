from rest_framework import serializers


class EMBEDDIATextSerializer(serializers.Serializer):
    text = serializers.CharField()
    #analyzers = serializers.MultipleChoiceField(choices=get_analyzer_choices(), default=["all"], required=False)


    #def validate(self, data):
    #    analyzer = data["analyzers"]
    #    if not analyzer:
    #        data["analyzers"] = ["all"]
    #    return data
