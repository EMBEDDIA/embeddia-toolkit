from rest_framework import generics, status, views
from rest_framework.response import Response
import shutil
import psutil
import re

from embeddia.serializers import EMBEDDIATextSerializer, EMBEDDIAGenerateTextSerializer
from embeddia_toolkit.settings import EMBEDDIA_ARTICLE_ANALYZER, EMBEDDIA_GENERATOR, EMBEDDIA_COMMENT_ANALYZER
from embeddia.exceptions import ServiceFailedException
from embeddia.analyzers.exceptions import ServiceNotAvailableError


class EMBEDDIARootView(generics.GenericAPIView):
    """
    EMBEDDIA root view. Displays all resources.
    """

    def get(self, request):
        path = re.sub(r"/$", "", request.path)
        mlp_info = {
            "Article Analyzer": request.build_absolute_uri(f"{path}/article_analyzer/"),
            "Comment Analyzer": request.build_absolute_uri(f"{path}/comment_analyzer/"),
            "Article Generator": request.build_absolute_uri(f"{path}/article_generator/"),
            "Health": request.build_absolute_uri(f"{path}/health/"),
        }
        return Response(mlp_info, status=status.HTTP_200_OK)


class EMBEDDIAHealthView(generics.GenericAPIView):
    """
    EMBEDDIA health view. Displays information about service"s health.
    """

    def get(self, request):
        disk_total, disk_used, disk_free = shutil.disk_usage("/")
        memory = psutil.virtual_memory()

        embeddia_health = {
            "service": "EMBEDDIA Toolkit API",
            "disk": {
                "free": disk_free / (2 ** 30),
                "total": disk_total / (2 ** 30),
                "used": disk_used / (2 ** 30),
                "unit": "GB"
            },
            "memory": {
                "free": memory.available / (2 ** 30),
                "total": memory.total / (2 ** 30),
                "used": memory.used / (2 ** 30),
                "unit": "GB"
            },
            "cpu": {
                "percent": psutil.cpu_percent()
            },
            "services": {}
        }

        # check health of services
        services = {**EMBEDDIA_ARTICLE_ANALYZER.analyzers, **EMBEDDIA_COMMENT_ANALYZER.analyzers}
        for service_name, service_class in services.items():
            try:
                service_status = service_class.check_health()
            except ServiceNotAvailableError:
               service_status = False
            # MLP package does not have check_health method and it's not really a service
            except AttributeError:
                service_status = None
            # do not include None from MLP package
            if service_status != None:
                embeddia_health["services"][service_name] = service_status

        return Response(embeddia_health, status=status.HTTP_200_OK)


class EMBEDDIAArticleAnalyzerView(generics.GenericAPIView):
    """
    EMBEDDIA Article Analyzer view.
    """
    serializer_class = EMBEDDIATextSerializer

    def post(self, request):
        serializer = EMBEDDIATextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data["text"]

        #try:
        processed = EMBEDDIA_ARTICLE_ANALYZER.process(text)
        #except Exception as e:
        #    raise ServiceFailedException(e)        
        return Response(processed, status=status.HTTP_200_OK)


class EMBEDDIACommentAnalyzerView(generics.GenericAPIView):
    """
    EMBEDDIA Article Analyzer view.
    """
    serializer_class = EMBEDDIATextSerializer

    def post(self, request):
        serializer = EMBEDDIATextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data["text"]

        #try:
        processed = EMBEDDIA_COMMENT_ANALYZER.process(text)
        #except Exception as e:
        #    raise ServiceFailedException(e)        
        return Response(processed, status=status.HTTP_200_OK)


class EMBEDDIAGeneratorsView(generics.GenericAPIView):
    """
    EMBEDDIA Generators view.
    """
    serializer_class = EMBEDDIAGenerateTextSerializer

    def post(self, request):
        serializer = EMBEDDIAGenerateTextSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        language = serializer.validated_data["language"]
        dataset = serializer.validated_data["dataset"]
        location = serializer.validated_data["location"]
        #try:
        processed = EMBEDDIA_GENERATOR.process(dataset, language, location)
        #except Exception as e:
        #    raise ServiceFailedException(e)
        return Response(processed, status=status.HTTP_200_OK)


#class EMBEDDIADashboardView(generics.GenericAPIView):

