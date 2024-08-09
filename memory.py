import os
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
from llama_index.core.indices.property_graph import DynamicLLMPathExtractor, \
    SimpleLLMPathExtractor, ImplicitPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.llms.gemini import Gemini
from utils import base_dir, disable_filters # also sets api key during module import




MEMORY_MAP = {
    'athena01': 7688,
    'artemis01': 7687
}
query_engine = None
with open(os.path.join(base_dir, "prompts/memory_query.txt"), "r",
          encoding='utf-8') as f:
    query_prompt = f.read()


def load_model():
    llm = Gemini(model_name="models/gemini-1.5-pro", safety_settings=disable_filters)
    embeddings = GeminiEmbedding(
        model_name='models/text-embedding-004')
    return llm, embeddings


def construct_graph(documents, character):
    graph_store = Neo4jPropertyGraphStore('neo4j', 'password', f'bolt://localhost:{MEMORY_MAP[character]}')
    llm, embeddings = load_model()
    index = PropertyGraphIndex.from_documents(
        documents,
        kg_extractors=[SimpleLLMPathExtractor(llm=llm), ImplicitPathExtractor()],
        embed_model=embeddings,
        llm=llm,
        property_graph_store=graph_store,
        show_progress=True,
    )
    return index


def load_graph(character):
    llm, embeddings = load_model()
    graph_store = Neo4jPropertyGraphStore('neo4j', 'password',
                                          f'bolt://localhost:{MEMORY_MAP[character]}')
    index = PropertyGraphIndex.from_existing(
        property_graph_store=graph_store,
        llm=llm,
        embed_model=embeddings,
    )
    query_engine = index.as_query_engine(llm=llm)
    return index, query_engine


def construct_memories():
    for character in MEMORY_MAP.keys():
        graph_store = Neo4jPropertyGraphStore('neo4j', 'password',
                                              f'bolt://localhost:{MEMORY_MAP[character]}')
        # Delete currente memories
        with graph_store._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print(f"Memory for {character} deleted.")

        # Generate memories
        documents = SimpleDirectoryReader(f"./memories/{character}").load_data()
        construct_graph(documents, character)
        print(f"Memory for {character} constructed and saved.")


if __name__ == '__main__':
    character = 'athena01'
    # documents = SimpleDirectoryReader(f"./memories/{character}").load_data()
    # index = construct_graph(documents, character)
    index, query_engine = load_graph(character)
    while True:
        query = input("Query: ")
        response = query_engine.query(query)
        print(response)
    #construct_memories()
    #print(MEMORY_MAP)


