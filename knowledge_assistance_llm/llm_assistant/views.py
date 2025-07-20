from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from knowledge_base.models import Document
from knowledge_base.utils import format_answer_markdown
from django.conf import settings
import os
import glob
import asyncio


def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

class AskQuestionView(APIView):
    def post(self, request):
        ensure_event_loop()

        question = request.data.get("question")
        
        if not question:
            return Response({'error': 'No question provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            document_count = Document.objects.all().count()
            if document_count == 0:
                return Response({
                    'error': 'No documents found in database. Please upload some documents first through the admin panel.'
                }, status=status.HTTP_404_NOT_FOUND)

            index_dir = os.path.join(settings.BASE_DIR, "faiss_index")
            if not os.path.exists(index_dir):
                return Response({
                    'error': f'Knowledge base index not found. {document_count} document(s) exist in database but index was not created. Please try re-uploading a document.'
                }, status=status.HTTP_404_NOT_FOUND)

            index_files = glob.glob(os.path.join(index_dir, "faiss_index_*"))
            if not index_files:
                return Response({
                    'error': f'FAISS index files not found. {document_count} document(s) exist but no index files were created. Please try re-uploading a document.'
                }, status=status.HTTP_404_NOT_FOUND)

            index_path = index_files[0]
            print(f"Loading FAISS index from: {index_path}")

            vectorstore = FAISS.load_local(
                index_path,
                GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
                allow_dangerous_deserialization=True
            )
            retriever = vectorstore.as_retriever()
            
            # Updated LLM configuration - using gemini-1.5-flash 
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                temperature=0.7,
               
            )
           
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                return_source_documents=True
            )

           
            result = qa_chain.invoke({"query": question})
            sources = []
            for doc in result['source_documents']:
                source_path = doc.metadata.get('source', '')
                page = doc.metadata.get('page', None)

                if source_path:
                    filename = os.path.basename(source_path)
                    if page is not None:
                        sources.append(f"{filename} - Page {page + 1}")  
                    else:
                        sources.append(filename)

            formatted_answer = format_answer_markdown(result['result'])
            
            return Response({
                "answer": formatted_answer,
                "sources": sources
            })
            
        except Exception as e:
            print(f"Error details: {str(e)}") 
            return Response({
                'error': f'Error processing question: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    