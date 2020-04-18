from rest_framework import generics, status, views
from rest_framework.response import Response

from embeddia.serializers import EMBEDDIATextSerializer
from embeddia.analyzers.analyzers import (
    EMBEDDIAAnalyzer,
    HSDAnalyzer,
    KWEAnalyzer,
    HybridTaggerAnalyzer
)
from embeddia_toolkit.settings import (
    HSD_HOST,
    KWE_HOST,
    NLG_HOST,
    HT_HOST
)

embeddia_analyzers = {
    "KWE": KWEAnalyzer(host=KWE_HOST),
    "HSD": HSDAnalyzer(host=HSD_HOST),
    "HT": HybridTaggerAnalyzer(host=HT_HOST)
}

EMBEDDIA_ANALYZER_OBJECT = EMBEDDIAAnalyzer(embeddia_analyzers=embeddia_analyzers)


class EMBEDDIATextView(generics.GenericAPIView):
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
        processed = EMBEDDIA_ANALYZER_OBJECT.process(text, analyzers=analyzers)
        return Response(processed, status=status.HTTP_200_OK)
