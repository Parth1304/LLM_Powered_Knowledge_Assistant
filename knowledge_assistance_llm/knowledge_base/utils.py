import asyncio
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from django.conf import settings
import re

def process_document(file_path, doc_name):
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".md", ".txt"]:
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type")

        pages = loader.load_and_split()

        try:
            asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.from_documents(pages, embeddings)

      
        safe_doc_name = "".join(c for c in doc_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_doc_name = safe_doc_name.replace(' ', '_')
        index_name = f"faiss_index_{safe_doc_name}"

        index_dir = os.path.join(settings.BASE_DIR, "faiss_index")
        os.makedirs(index_dir, exist_ok=True)

        index_path = os.path.join(index_dir, index_name)
        vectorstore.save_local(index_path)

        print(f"✅ Successfully processed document: {doc_name}")
        print(f"📦 FAISS index saved to: {index_path}")

    except Exception as e:
        print(f"❌ Error processing document {doc_name}: {str(e)}")
        raise e




def format_answer_markdown(answer: str) -> str:
   
    # Remove markdown headers like ### and bold markers like **
    answer = re.sub(r'#+\s*', '', answer)                   # Remove '### '
    answer = re.sub(r'\*\*(.*?)\*\*', r'\1', answer)        # Remove '**bold**'

    # Replace list bullets with dashes or just space
    answer = re.sub(r'^\s*[\*\-]\s*', '- ', answer, flags=re.MULTILINE)

    # Convert line breaks to spaces
    answer = answer.replace('\n', ' ')

    # Normalize multiple spaces
    answer = re.sub(r'\s{2,}', ' ', answer)

    # Capitalize after sentence endings
    answer = re.sub(r'(?<=[.!?])\s+([a-z])', lambda m: ' ' + m.group(1).upper(), answer)

    # Capitalize first letter
    if answer:
        answer = answer[0].upper() + answer[1:]

    return answer.strip()
