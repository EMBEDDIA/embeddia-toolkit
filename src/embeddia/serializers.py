from rest_framework import serializers


class EMBEDDIATextSerializer(serializers.Serializer):
    text = serializers.CharField()
