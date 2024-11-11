from langchain_ollama import ChatOllama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import json
import html2text


if __name__ == '__main__':
    with open('emails.json', 'r') as file:
        data = json.load(file)

    emails = data['value']
    counter = 1
    docs = []
    for email in emails:
        body = html2text.html2text(email["body"]['content'])
        docs.append(Document(page_content=body))

    llm = ChatOllama(temperature=0, model="llama3.1:8b")

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    print(summary)
