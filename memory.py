import os

from llama_index.core.graph_stores import EntityNode, Relation
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import PropertyGraphIndex, SimpleDirectoryReader
from llama_index.core.indices.property_graph import DynamicLLMPathExtractor, \
    SimpleLLMPathExtractor, ImplicitPathExtractor, LLMSynonymRetriever, VectorContextRetriever
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.llms.gemini import Gemini
from utils import base_dir, disable_filters # also sets api key during module import
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import TextNode


MEMORY_MAP = {
    'aphrodite01': 7687,
    'apollo01': 7688,
    'ares01': 7689,
    'artemis01': 7690,
    'athena01': 7691,
    'demeter01': 7692,
    'hephaestus01': 7693,
    'hera01': 7694,
    'hermes01': 7695,
    'hestia01': 7696,
    'poseidon01': 7697,
    'zeus01': 7698
}


query_engine = None
index = None
with open(os.path.join(base_dir, "prompts/memory_query.txt"), "r",
          encoding='utf-8') as f:
    query_prompt = f.read()


def load_model():
    #llm = Gemini(model_name="models/gemini-1.5-pro", safety_settings=disable_filters)
    llm = Gemini(model_name="models/gemini-1.5-flash", safety_settings=disable_filters)
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


def store_new_memory(index: PropertyGraphIndex, text_block: str):
    # Create a new document from the text block
    new_document = Document(text=text_block)

    # Parse the new document into nodes
    parser = SimpleNodeParser.from_defaults(
        chunk_size=512,
        chunk_overlap=20
    )
    nodes = parser.get_nodes_from_documents([new_document])

    if not nodes:
        print("No nodes were created from the text block. The memory might be too short or couldn't be parsed.")
        return index

    # Use the index's kg_extractors to extract entities and relations
    for extractor in index._kg_extractors:
        nodes = extractor(nodes)

    # Retrieve existing related information
    retriever = index.as_retriever(
        sub_retrievers=[
            LLMSynonymRetriever(index.property_graph_store, llm=index._llm),
            VectorContextRetriever(index.property_graph_store, embed_model=index._embed_model)
        ]
    )
    related_nodes = retriever.retrieve(text_block)

    # Process and add new nodes and relations
    for node in nodes:
        # Add new node
        text_node = TextNode(text=node.get_content())
        index.property_graph_store.upsert_llama_nodes([text_node])

        # Process extracted entities and relations
        entities = node.metadata.get("kg_nodes", [])
        relations = node.metadata.get("kg_relations", [])

        # Add entities
        for entity in entities:
            entity_node = EntityNode(
                name=entity.name,
                label=entity.label,
                properties=entity.properties
            )
            index.property_graph_store.upsert_nodes([entity_node])

            # Connect entity to text node
            source_relation = Relation(
                label="HAS_SOURCE",
                source_id=entity_node.id,
                target_id=text_node.id
            )
            index.property_graph_store.upsert_relations([source_relation])

        # Add relations
        for relation in relations:
            index.property_graph_store.upsert_relations([
                Relation(
                    label=relation.label,
                    source_id=relation.source_id,
                    target_id=relation.target_id,
                    properties=relation.properties
                )
            ])

    print("New memory integrated into the graph with connections to existing knowledge.")

    return index


if __name__ == '__main__':
    character = 'athena01'
    # documents = SimpleDirectoryReader(f"./memories/{character}").load_data()
    # index = construct_graph(documents, character)
    # index, query_engine = load_graph(character)
    # while True:
    #     query = input("Query: ")
    #     response = query_engine.query(query)
    #     print(response)
    construct_memories()
    #print(MEMORY_MAP)


