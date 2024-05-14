import argparse
from .query import setup_chain, interact_with_pdfs

def main():
    """Main function to run the PDF query interaction."""
    parser = argparse.ArgumentParser(description="PDF Interaction with LangChain")
    parser.add_argument('--llm_model', type=str, default='llama3:instruct', help='The LLM model to use')
    parser.add_argument('--embed_model', type=str, default='nomic-embed-text', help='The embedding model to use')
    parser.add_argument('--pdf_directory', type=str, default='docs/resources', help='Directory containing PDF files')

    args = parser.parse_args()
    
    print(f"Arguments received: llm_model={args.llm_model}, embed_model={args.embed_model}, pdf_directory={args.pdf_directory}")

    chain = setup_chain(args.llm_model, args.embed_model, args.pdf_directory)
    
    while True:
        query = input("Enter your query (type 'exit', 'q' or '/exit' to quit): ")
        if query.lower() in ['exit', 'q', '/exit']:
            break
        response = interact_with_pdfs(chain, query)
        print(f'Response: {response}')

if __name__ == '__main__':
    main()


