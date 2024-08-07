import os
import time

from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
from llama_index.core.indices.property_graph import DynamicLLMPathExtractor, \
    SimpleLLMPathExtractor, ImplicitPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.llms.gemini import Gemini
from utils import base_dir # also sets api key during module import


llm = Gemini(model_name="models/gemini-1.5-pro")
embeddings = GeminiEmbedding(
    model_name='models/text-embedding-004')
MEMORY_MAP = {
    'athena01': Neo4jPropertyGraphStore('neo4j', 'password', 'bolt://localhost:7688'),
    'artemis01': Neo4jPropertyGraphStore('neo4j', 'password', 'bolt://localhost:7687'),
}
query_engine = None
with open(os.path.join(base_dir, "prompts/memory_query.txt"), "r",
          encoding='utf-8') as f:
    query_prompt = f.read()


def construct_graph(documents, graph_store):
    index = PropertyGraphIndex.from_documents(
        documents,
        kg_extractors=[SimpleLLMPathExtractor(llm=llm), ImplicitPathExtractor()],
        embed_model=embeddings,
        llm=llm,
        property_graph_store=graph_store,
        show_progress=True,
    )
    return index


def load_graph(graph_store):
    index = PropertyGraphIndex.from_existing(
        property_graph_store=graph_store,
        llm=llm,
        embed_model=embeddings,
    )
    query_engine = index.as_query_engine(llm=llm)
    return index, query_engine


def construct_memories():
    # Delete currente memories
    for character in MEMORY_MAP:
        with MEMORY_MAP[character]._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print(f"Memory for {character} deleted.")
    
    # Create memories
    for character in MEMORY_MAP:
        documents = SimpleDirectoryReader(f"./memories/{character}").load_data()
        index = construct_graph(documents, MEMORY_MAP[character])
        print(f"Memory for {character} constructed and saved.")


if __name__ == '__main__':
    # character = 'athena01'
    # documents = SimpleDirectoryReader(f"./memories/{character}").load_data()
    # #index = construct_graph(documents, MEMORY_MAP[character])
    # index, query_engine = load_graph(MEMORY_MAP[character])
    # while True:
    #     query = input("Query: ")
    #     response = query_engine.query(query)
    #     print(response)
    #construct_memories()
    print(MEMORY_MAP)

