from rest_framework import generics, status, views
from rest_framework.response import Response
from celery import group
from texta_mlp.mlp import MLP
import shutil
import psutil
import re

from .serializers import EMBEDDIAArticleSerializer, EMBEDDIACommentSerializer
from .exceptions import ServiceFailedException
from .analyzers.exceptions import ServiceNotAvailableError
from . import exceptions

from embeddia_toolkit.taskman import apply_single_analyzer
from embeddia_toolkit.settings import DATA_DIR, MLP_LANGS, ARTICLE_ANALYZERS, COMMENT_ANALYZERS

mlp = MLP(language_codes=MLP_LANGS, resource_dir=DATA_DIR)


def analyze_article(analyzer_names, text, mlp_name="TEXTA MLP"):
    mlp_analysis = mlp.process(text)
    # default to all analyzers
    if not analyzer_names:
        analyzer_names = list(ARTICLE_ANALYZERS.keys())
    else:
        analyzer_names = list(analyzer_names)
    # extract stuff from MLP output
    tokenized_text = mlp_analysis["text"]["text"]
    language = mlp_analysis["text"]["language"]["analysis"]
    lemmas = mlp_analysis["text"]["lemmas"]
    entities = [{"entity": e["str_val"], "type": e["fact"], "source": mlp_name} for e in mlp_analysis["texta_facts"]]
    # use analyzers
    tags = []
    group_task = group([apply_single_analyzer.s(analyzer_name, lemmas) for analyzer_name in analyzer_names])
    group_results = group_task.apply_async()
    # get tags
    tags = []
    for i,analyzer_tags in enumerate(group_results.get()):
        for tag in analyzer_tags:
            tag["source"] = analyzer_names[i]
            tags.append(tag)
    # prepare output
    output = {
        "text": tokenized_text,
        "tags": tags,
        "entities": entities,
        "language": language,
        "analyzers": analyzer_names+[mlp_name]
    }
    return output


def analyze_comment(analyzer_names, text):
    tags = []
    # select analyzers
    # default to all analyzers
    if not analyzer_names:
        analyzer_names = list(COMMENT_ANALYZERS.keys())
    else:
        analyzer_names = list(analyzer_names)
    # use analyzers
    tags = []
    group_task = group([apply_single_analyzer.s(analyzer_name, text) for analyzer_name in analyzer_names])
    group_results = group_task.apply_async()
    # get tags
    tags = []
    for i,analyzer_tags in enumerate(group_results.get()):
        for tag in analyzer_tags:
            tag["source"] = analyzer_names[i]
            tags.append(tag)
    # prepare output
    output = {
        "tags": tags,
        "text": text,
        "analyzers": analyzer_names}
    return output


class EMBEDDIARootView(generics.GenericAPIView):
    """
    EMBEDDIA root view. Displays all resources.
    """

    def get(self, request):
        path = re.sub(r"/$", "", request.path)
        mlp_info = {
            "Article Analyzer": request.build_absolute_uri(f"{path}/article_analyzer/"),
            "Comment Analyzer": request.build_absolute_uri(f"{path}/comment_analyzer/"),
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
        services = {**ARTICLE_ANALYZERS, **COMMENT_ANALYZERS}
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
    serializer_class = EMBEDDIAArticleSerializer

    def post(self, request):
        serializer = EMBEDDIAArticleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data["text"]
        analyzer_names = serializer.validated_data["analyzers"]
        processed = analyze_article(analyzer_names, text)    
        return Response(processed, status=status.HTTP_200_OK)


class EMBEDDIACommentAnalyzerView(generics.GenericAPIView):
    """
    EMBEDDIA Article Analyzer view.
    """
    serializer_class = EMBEDDIACommentSerializer

    def post(self, request):
        serializer = EMBEDDIACommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        text = serializer.validated_data["text"]
        analyzer_names = serializer.validated_data["analyzers"]
        processed = analyze_comment(analyzer_names, text)
        return Response(processed, status=status.HTTP_200_OK)
