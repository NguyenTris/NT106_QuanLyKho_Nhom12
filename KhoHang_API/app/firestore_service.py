"""firestore_service.py

Simple Firestore helper for saving item documents.

Usage:
 - Ensure `GOOGLE_APPLICATION_CREDENTIALS` is set or ADC is available.
 - install `google-cloud-firestore`.
"""
from typing import Any, Dict
import logging

try:
    from google.cloud import firestore
except Exception:  # pragma: no cover - optional dependency
    firestore = None

logger = logging.getLogger(__name__)


def get_client():
    """Return Firestore client or None if unavailable."""
    if firestore is None:
        logger.warning("google-cloud-firestore not installed")
        return None
    try:
        return firestore.Client()
    except Exception as e:
        logger.exception("Failed to create Firestore client: %s", e)
        return None


def save_item(item: Dict[str, Any]) -> bool:
    """Save or overwrite an item document in `items` collection.

    Args:
        item: dict containing at least an `id` key

    Returns:
        True if saved, False otherwise
    """
    client = get_client()
    if client is None:
        return False

    doc_id = str(item.get("id"))
    if not doc_id:
        logger.error("Item missing id: %s", item)
        return False

    try:
        client.collection("items").document(doc_id).set(item)
        return True
    except Exception:
        logger.exception("Failed to save item to Firestore: %s", item)
        return False


def update_item(item_id: int, data: Dict[str, Any]) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("items").document(str(item_id)).update(data)
        return True
    except Exception:
        logger.exception("Failed to update item %s in Firestore", item_id)
        return False


def delete_item(item_id: int) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("items").document(str(item_id)).delete()
        return True
    except Exception:
        logger.exception("Failed to delete item %s from Firestore", item_id)
        return False


def get_all_items() -> list:
    client = get_client()
    if client is None:
        return []
    try:
        docs = client.collection("items").stream()
        return [d.to_dict() for d in docs]
    except Exception:
        logger.exception("Failed to fetch items from Firestore")
        return []


def get_stock_out_records() -> list:
    client = get_client()
    if client is None:
        return []
    try:
        docs = client.collection("stock_out").order_by("created_at", direction="DESCENDING").stream()
        return [d.to_dict() | {"id": d.id} for d in docs]
    except Exception:
        logger.exception("Failed to fetch stock_out records from Firestore")
        return []


def get_stock_out_record(record_id: str) -> dict | None:
    client = get_client()
    if client is None:
        return None
    try:
        doc = client.collection("stock_out").document(record_id).get()
        if not doc.exists:
            return None
        return doc.to_dict() | {"id": doc.id}
    except Exception:
        logger.exception("Failed to get stock_out record %s from Firestore", record_id)
        return None


def save_stock_out(record_id: str, data: Dict[str, Any]) -> bool:
    client = get_client()
    if client is None:
        return False


def save_stock_in(record_id: str, data: Dict[str, Any]) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("stock_in").document(record_id).set(data)
        return True
    except Exception:
        logger.exception("Failed to save stock_in %s to Firestore", record_id)
        return False


def get_stock_in_records() -> list:
    client = get_client()
    if client is None:
        return []
    try:
        docs = client.collection("stock_in").order_by("created_at", direction="DESCENDING").stream()
        return [d.to_dict() | {"id": d.id} for d in docs]
    except Exception:
        logger.exception("Failed to fetch stock_in records from Firestore")
        return []


def delete_stock_in(record_id: str) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("stock_in").document(record_id).delete()
        return True
    except Exception:
        logger.exception("Failed to delete stock_in %s from Firestore", record_id)
        return False
    try:
        client.collection("stock_out").document(record_id).set(data)
        return True
    except Exception:
        logger.exception("Failed to save stock_out %s to Firestore", record_id)
        return False


def delete_stock_out(record_id: str) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("stock_out").document(record_id).delete()
        return True
    except Exception:
        logger.exception("Failed to delete stock_out %s from Firestore", record_id)
        return False


def get_all_suppliers() -> list:
    client = get_client()
    if client is None:
        return []
    try:
        docs = client.collection("suppliers").stream()
        return [d.to_dict() | {"id": d.id} for d in docs]
    except Exception:
        logger.exception("Failed to fetch suppliers from Firestore")
        return []


def save_supplier(supplier_id: str, data: Dict[str, Any]) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("suppliers").document(str(supplier_id)).set(data)
        return True
    except Exception:
        logger.exception("Failed to save supplier %s to Firestore", supplier_id)
        return False


def delete_supplier(supplier_id: str) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("suppliers").document(str(supplier_id)).delete()
        return True
    except Exception:
        logger.exception("Failed to delete supplier %s from Firestore", supplier_id)
        return False


def get_all_warehouses() -> list:
    client = get_client()
    if client is None:
        return []
    try:
        docs = client.collection("warehouses").stream()
        return [d.to_dict() | {"id": d.id} for d in docs]
    except Exception:
        logger.exception("Failed to fetch warehouses from Firestore")
        return []


def save_warehouse(warehouse_id: str, data: Dict[str, Any]) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("warehouses").document(str(warehouse_id)).set(data)
        return True
    except Exception:
        logger.exception("Failed to save warehouse %s to Firestore", warehouse_id)
        return False


def delete_warehouse(warehouse_id: str) -> bool:
    client = get_client()
    if client is None:
        return False
    try:
        client.collection("warehouses").document(str(warehouse_id)).delete()
        return True
    except Exception:
        logger.exception("Failed to delete warehouse %s from Firestore", warehouse_id)
        return False

