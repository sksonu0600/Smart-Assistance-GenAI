import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

class MedicalReportAnalyzer:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Use the correct model name
        
        # Configure embeddings with correct model name
        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key=api_key,
            model="models/embedding-001"  # Fixed model name format
        )
    
    def analyze_report(self, text):
        try:
            # Split text into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_text(text)
            
            # Create vector store for chunks
            vectorstore = FAISS.from_texts(chunks, self.embeddings)
            
            # Generate analysis with structured prompt
            prompt = """As a medical report analyzer, please provide a detailed analysis with the following structure:

            1. Key Findings:
            - List all major observations
            - Highlight any abnormal results
            - Note critical values

            2. Diagnosis Summary:
            - Primary diagnosis
            - Secondary conditions
            - Risk factors identified

            3. Recommended Actions:
            - Immediate steps needed
            - Follow-up requirements
            - Lifestyle modifications
            - Medication recommendations

            4. Medical Terms Explained:
            - Define technical terminology
            - Provide patient-friendly explanations

            Medical Report Text:
            """
            
            response = self.model.generate_content(
                prompt + text,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            return {
                'analysis': response.text,
                'chunks': len(chunks),
                'document_length': len(text)
            }
            
        except Exception as e:
            raise Exception(f"Analysis error: {str(e)}")