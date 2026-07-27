import chromadb

CHROMA_PATH = "knowledge/vector_store/"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH),
)

collections = client.list_collections()

print(collections)

# for collection_summary in collections:
#     collection = client.get_collection(
#         name=collection_summary.name,
#     )

#     print("\nCollection:", collection.name)
#     print("Stored chunks:", collection.count()) 