from typing import Any, Optional
from spec_weaver.adapters.doorstop import _get_custom_attribute, _get_git_file_date
from spec_weaver.core.review_state import ReviewState

IMPL_STATUS_BADGE: dict[str, str] = {
    "draft": "📝 draft",
    "in-progress": "🚧 in-progress",
    "implemented": "✅ implemented",
    "deprecated": "🗑️ deprecated",
}

def get_impl_status_badge(item: Any) -> str:
    """YAMLの status フィールドを絵文字バッジ文字列に変換する。未設定は '-'。"""
    status = _get_custom_attribute(item, "status", None)
    if not status:
        return "-"
    return IMPL_STATUS_BADGE.get(str(status), f"{status}")

def get_review_status_badge(item_or_id: str | Any, review_state: Optional[ReviewState] = None) -> str:
    """DoorstopのレビューステータスまたはGherkin Featureのステータスをバッジ文字列に変換する。"""
    if review_state:
        uid = str(getattr(item_or_id, "uid", item_or_id))
        return review_state.get_status(uid)
    return "✅ reviewed"

def get_timestamp(item: Any, key: str) -> str:
    """タイムスタンプを取得する。Git履歴 → YAML属性 → '-' の優先順位。"""
    file_path = getattr(item, "path", None)
    if file_path:
        mode = "first" if key == "created_at" else "latest"
        git_date = _get_git_file_date(str(file_path), mode=mode)
        if git_date:
            return git_date
    val = _get_custom_attribute(item, key, None)
    return str(val) if val else "-"

def get_uid_prefix(uid: str) -> str:
    """'REQ-001' → 'REQ'、'AUTH-REQ-001' → 'AUTH-REQ'"""
    import re
    m = re.match(r"^(.*)-\d+$", uid)
    return m.group(1) if m else uid
