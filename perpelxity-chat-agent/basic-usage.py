# Initialize the system
pdf_qa = PDFQuestionAnswering()

# Process your PDFs
pdf_files = ["research_paper.pdf", "manual.pdf"]
pdf_qa.process_pdfs_and_setup(pdf_files)

# Ask questions
response = pdf_qa.ask_question("What is the main conclusion of the research?")
print(response['answer'])

###
# Using Existing Vector
###

# If you've already processed documents and saved the vector store
pdf_qa = PDFQuestionAnswering()
pdf_qa.load_vectorstore("faiss_index")
pdf_qa.setup_qa_chain()

# Now you can ask questions without reprocessing documents
response = pdf_qa.ask_question("Summarize the methodology")

###
# Using ChromaDB Alternative
###

# For better persistence, use the ChromaDB version
pdf_qa_chroma = PDFQuestionAnsweringChroma()

# Process documents (this will be saved automatically)
documents = pdf_qa_chroma.load_pdf_documents(["document.pdf"])
split_docs = pdf_qa_chroma.split_documents(documents)
pdf_qa_chroma.create_vectorstore_chroma(split_docs)
