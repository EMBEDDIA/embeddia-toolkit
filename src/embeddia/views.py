from rest_framework import generics, status, views
from rest_framework.response import Response

from embeddia.serializers import EMBEDDIATextSerializer
from embeddia.analyzers.analyzers import EMBEDDIAAnalyzer


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
        embeddia_analyzer = EMBEDDIAAnalyzer()
        processed = embeddia_analyzer.process(text)
        return Response(processed, status=status.HTTP_200_OK)
