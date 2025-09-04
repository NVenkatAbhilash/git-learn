import os
import getpass
from typing import List
from dotenv import load_dotenv

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# Load environment variables
load_dotenv()


class PDFQuestionAnswering:
    def __init__(self):
        """Initialize the PDF Question Answering system."""
        self.setup_api_keys()
        self.setup_models()
        self.vectorstore = None
        self.qa_chain = None

    def setup_api_keys(self):
        """Setup API keys for Google Gemini and OpenAI."""
        # Setup Google API key for Gemini
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

        # Setup OpenAI API key for embeddings
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    def setup_models(self):
        """Initialize the LLM and embedding models."""
        # Initialize Gemini 2.0 Flash model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001",  # Using the specific model you requested
            temperature=0.1,  # Low temperature for more factual responses
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",  # Latest and most capable embedding model
            chunk_size=1000
        )

    def load_pdf_documents(self, pdf_paths: List[str]) -> List[Document]:
        """
        Load and process PDF documents.

        Args:
            pdf_paths: List of paths to PDF files

        Returns:
            List of Document objects
        """
        documents = []

        for pdf_path in pdf_paths:
            print(f"Loading PDF: {pdf_path}")

            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(pdf_path)
            pdf_documents = loader.load()

            documents.extend(pdf_documents)

        print(f"Loaded {len(documents)} pages from {len(pdf_paths)} PDF(s)")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better processing.

        Args:
            documents: List of Document objects

        Returns:
            List of split Document objects
        """
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Maximum characters per chunk
            chunk_overlap=200,  # Overlap between chunks to maintain context
            length_function=len,  # Function to measure chunk length
            separators=["\n\n", "\n", " ", ""]  # Preferred splitting points
        )

        # Split documents
        split_docs = text_splitter.split_documents(documents)
        print(f"Split into {len(split_docs)} chunks")

        return split_docs

    def create_vectorstore(self, documents: List[Document], persist_path: str = None):
        """
        Create vector store from documents.

        Args:
            documents: List of Document objects
            persist_path: Optional path to persist the vector store
        """
        print("Creating embeddings and vector store...")

        # Create FAISS vector store
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

        # Optionally save the vector store
        if persist_path:
            self.vectorstore.save_local(persist_path)
            print(f"Vector store saved to {persist_path}")

        print("Vector store created successfully!")

    def load_vectorstore(self, persist_path: str):
        """
        Load an existing vector store from disk.

        Args:
            persist_path: Path to the saved vector store
        """
        try:
            self.vectorstore = FAISS.load_local(
                persist_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from {persist_path}")
        except Exception as e:
            print(f"Error loading vector store: {e}")
            raise

    def setup_qa_chain(self):
        """Setup the question-answering chain."""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized. Please create or load a vector store first.")

        # Create retriever from vector store
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}  # Number of documents to retrieve
        )

        # Create system prompt for the QA chain
        system_prompt = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.
        
        Context: {context}"""

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # Create document processing chain
        question_answer_chain = create_stuff_documents_chain(
            self.llm,
            prompt
        )

        # Create retrieval chain
        self.qa_chain = create_retrieval_chain(
            retriever,
            question_answer_chain
        )

        print("QA chain setup complete!")

    def ask_question(self, question: str) -> dict:
        """
        Ask a question and get an answer based on the loaded documents.

        Args:
            question: The question to ask

        Returns:
            Dictionary containing the answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Please setup the QA chain first.")

        print(f"Question: {question}")
        print("Thinking...")

        # Get response from the chain
        response = self.qa_chain.invoke({"input": question})

        return response

    def process_pdfs_and_setup(self, pdf_paths: List[str], persist_path: str = "faiss_index"):
        """
        Complete workflow to process PDFs and setup QA system.

        Args:
            pdf_paths: List of PDF file paths
            persist_path: Path to save/load vector store
        """
        # Load PDF documents
        documents = self.load_pdf_documents(pdf_paths)

        # Split documents into chunks
        split_docs = self.split_documents(documents)

        # Create vector store
        self.create_vectorstore(split_docs, persist_path)

        # Setup QA chain
        self.setup_qa_chain()

        print("PDF processing and QA setup complete!")


# Example usage and demonstration
def main():
    """Main function demonstrating the usage of the PDFQuestionAnswering class."""

    # Initialize the QA system
    pdf_qa = PDFQuestionAnswering()

    # Example PDF paths (replace with your actual PDF paths)
    pdf_files = [
        "document1.pdf",
        "document2.pdf",
        # Add more PDF paths as needed
    ]

    try:
        # Process PDFs and setup QA system
        pdf_qa.process_pdfs_and_setup(pdf_files)

        # Ask questions
        questions = [
            "What is the main topic of the document?",
            "Can you summarize the key points?",
            "What are the conclusions mentioned?",
        ]

        for question in questions:
            response = pdf_qa.ask_question(question)

            print(f"\nQuestion: {question}")
            print(f"Answer: {response['answer']}")
            print(f"Sources: {len(response['context'])} documents")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {e}")


# Alternative implementation with ChromaDB (more persistent)
class PDFQuestionAnsweringChroma:
    """Alternative implementation using ChromaDB for persistence."""

    def __init__(self):
        self.setup_api_keys()
        self.setup_models()
        self.vectorstore = None

    def setup_api_keys(self):
        """Setup API keys."""
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

    def setup_models(self):
        """Initialize models."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-001",
            temperature=0.1,
        )

        # For ChromaDB, we can use the default embedding function or specify our own
        # Here we'll use a simpler approach without OpenAI embeddings

    def create_vectorstore_chroma(self, documents: List[Document], persist_dir: str = "./chroma_db"):
        """Create ChromaDB vector store."""
        from langchain_community.vectorstores import Chroma

        self.vectorstore = Chroma.from_documents(
            documents=documents,
            persist_directory=persist_dir
        )

        print(f"ChromaDB vector store created in {persist_dir}")

    def load_vectorstore_chroma(self, persist_dir: str = "./chroma_db"):
        """Load existing ChromaDB vector store."""
        from langchain_community.vectorstores import Chroma

        self.vectorstore = Chroma(
            persist_directory=persist_dir
        )

        print(f"ChromaDB vector store loaded from {persist_dir}")


# Utility function for batch processing
def batch_process_pdfs(pdf_directory: str, output_vectorstore: str = "faiss_index"):
    """
    Process all PDFs in a directory.

    Args:
        pdf_directory: Directory containing PDF files
        output_vectorstore: Path to save the vector store
    """
    import glob

    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_directory}")
        return

    print(f"Found {len(pdf_files)} PDF files")

    # Initialize and process
    pdf_qa = PDFQuestionAnswering()
    pdf_qa.process_pdfs_and_setup(pdf_files, output_vectorstore)

    return pdf_qa


if __name__ == "__main__":
    # Run the main demonstration
    main()

    # Example of batch processing
    # pdf_qa_system = batch_process_pdfs("./pdfs/", "my_vectorstore")
