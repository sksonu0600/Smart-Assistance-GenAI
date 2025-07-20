from PyPDF2 import PdfReader
import io

class PDFProcessor:
    def extract_text(self, file):
        """
        Extract text content from a PDF file
        
        Args:
            file: File object containing PDF data
            
        Returns:
            str: Extracted text from the PDF
            
        Raises:
            Exception: If PDF processing fails
        """
        try:
            # Create BytesIO object from file content
            file_stream = io.BytesIO(file.read())
            
            # Create PDF reader object
            reader = PdfReader(file_stream)
            
            # Extract text from all pages
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            # Verify text extraction
            if not text.strip():
                raise ValueError("No text content extracted from PDF")
                
            return text
            
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def get_metadata(self, file):
        """
        Extract metadata from PDF file
        
        Args:
            file: File object containing PDF data
            
        Returns:
            dict: PDF metadata
        """
        try:
            file_stream = io.BytesIO(file.read())
            reader = PdfReader(file_stream)
            return reader.metadata
        except Exception as e:
            raise Exception(f"Error extracting metadata: {str(e)}")