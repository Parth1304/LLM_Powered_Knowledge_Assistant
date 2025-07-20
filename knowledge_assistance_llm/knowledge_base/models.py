from django.db import models
from .utils import process_document
import os

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
           
            file_path = self.file.path
            print(f"✅ Processing document: {self.name} at path: {file_path}")

            if not os.path.exists(file_path):
                print(f"❌ File does not exist at {file_path}")
                return

            process_document(file_path, self.name)
            print(f"✅ Document processing completed for: {self.name}")

        except Exception as e:
            print(f"❌ Error in Document.save() for {self.name}: {str(e)}")