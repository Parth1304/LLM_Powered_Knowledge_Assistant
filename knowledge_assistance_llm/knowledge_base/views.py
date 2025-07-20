from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document

# Create your views here.
class DocumentListView(APIView):
    def get(self, request):
        try:
            documents = Document.objects.all()  # type: ignore[attr-defined]
            document_list = []
            for doc in documents:
                document_list.append({
                    'id': doc.id,
                    'name': doc.name,
                    'uploaded_at': doc.uploaded_at
                })
            
            return Response({
                'documents': document_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
