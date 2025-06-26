import requests
from config import config as cfg

headers = {
    'Authorization': f"Bearer {cfg.YONOTE_TOKEN}",
    'Content-Type': 'application/json'
}


async def get_collections():
    endpoint = "https://app.yonote.ru/api/collections.list"
    responce = requests.get(url=endpoint, headers=headers).json()
    return responce


async def get_collection_id_by_urlId(urlId: str) -> str | None:
    collections = await get_collections()

    if not collections["ok"]:
        print("Error getting collections")
        return None

    if collections["count"] == 0:
        print("No collections found")
        return None

    for collection in collections["data"]:
        if collection["urlId"] == urlId:
            return collection["id"]


async def get_documents():
    endpoint = "https://app.yonote.ru/api/documents.list"
    responce = requests.get(url=endpoint, headers=headers).json()
    return responce


async def get_document_id_by_urlId(urlId: str) -> str | None:
    documents = await get_documents()

    if not documents["ok"]:
        print("Error getting documents")
        return None

    if documents["total"] == 0:
        print("No documents found")
        return None

    for document in documents["data"]:
        if document["urlId"] == urlId:
            return document["id"]


async def create_document(collectionUrlId: str, title: str, text: str = None, parentDocumentUrlId: str = None, publish: bool = False):
    endpoint = "https://app.yonote.ru/api/documents.create"

    collection_id = await get_collection_id_by_urlId(collectionUrlId)
    parentDocumentId = await get_document_id_by_urlId(parentDocumentUrlId)

    if not collection_id:
        print("Collection not found")
        return None

    body = {
        "title": title,
        "collectionId": collection_id,
        "publish": publish
    }

    if text:
        body["text"] = text

    if parentDocumentId:
        body["parentDocumentId"] = parentDocumentId

    response = requests.post(url=endpoint, headers=headers, json=body)

    return response.json()
