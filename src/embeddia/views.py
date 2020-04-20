from rest_framework import generics, status, views
from rest_framework.response import Response
import re

from embeddia.serializers import EMBEDDIATextSerializer, EMBEDDIAGenerateTextSerializer
from embeddia_toolkit.settings import EMBEDDIA_ANALYZERS, EMBEDDIA_EU_GENERATOR
from embeddia.analyzers.analyzers import EMBEDDIAAnalyzer
from embeddia.exceptions import ServiceFailedException


EMBEDDIA_ANALYZER_OBJECT = EMBEDDIAAnalyzer(embeddia_analyzers=EMBEDDIA_ANALYZERS)
EMBEDDIA_GENERATOR_OBJECT = EMBEDDIA_EU_GENERATOR


class EMBEDDIARootView(generics.GenericAPIView):
    """
    EMBEDDIA root view. Displays all resources.
    """

    def get(self, request):
        path = re.sub(r"/$", "", request.path)
        mlp_info = {
            "Analyzers": request.build_absolute_uri(f"{path}/analyzers/"),
            "Generators": request.build_absolute_uri(f"{path}/generators/"),
        }
        return Response(mlp_info, status=status.HTTP_200_OK)


class EMBEDDIAAnalyzersView(generics.GenericAPIView):
    """
    View for analyzing a single piece of text.
    """
    serializer_class = EMBEDDIATextSerializer

    def post(self, request):
        serializer = EMBEDDIATextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data["text"]
        analyzers = list(serializer.validated_data["analyzers"])
        try:
            processed = EMBEDDIA_ANALYZER_OBJECT.process(text, analyzers=analyzers)
        except Exception as e:
            raise ServiceFailedException(e)        
        return Response(processed, status=status.HTTP_200_OK)


class EMBEDDIAGeneratorsView(generics.GenericAPIView):
    serializer_class = EMBEDDIAGenerateTextSerializer

    def post(self, request):
        serializer = EMBEDDIAGenerateTextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        language = serializer.validated_data["language"]
        dataset = serializer.validated_data["dataset"]
        location = serializer.validated_data["location"]
        try:
            processed = EMBEDDIA_EU_GENERATOR.process(dataset, language, location)
        except Exception as e:
            raise ServiceFailedException(e)
        return Response(processed, status=status.HTTP_200_OK)
