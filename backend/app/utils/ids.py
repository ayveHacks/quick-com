from typing import Any

from bson import ObjectId


def to_object_id(value: str | ObjectId) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    return ObjectId(value)


def serialize_document(document: dict[str, Any] | None) -> dict[str, Any] | None:
    if document is None:
        return None

    serialized: dict[str, Any] = {}
    for key, value in document.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, list):
            serialized[key] = [str(item) if isinstance(item, ObjectId) else item for item in value]
        else:
            serialized[key] = value
    return serialized

