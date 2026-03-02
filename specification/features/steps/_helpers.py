"""共通ヘルパー: Doorstop プロジェクト作成・CLI 実行・feature ファイル作成など。"""

from __future__ import annotations

import os
import subprocess
import textwrap
from pathlib import Path
from typing import Any

import yaml

# ──────────────────────────────────────────────
# 定数
# ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # spec-weaver root


# ──────────────────────────────────────────────
# CLI ユーティリティ
# ──────────────────────────────────────────────


def run_spec_weaver(
    args: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess:
    """spec-weaver CLI を uv run 経由で実行し、結果を返す。"""
    return subprocess.run(
        ["uv", "run", "spec-weaver"] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd or PROJECT_ROOT),
    )


# ──────────────────────────────────────────────
# .feature ファイル作成
# ──────────────────────────────────────────────


def write_feature_file(path: Path, content: str) -> None:
    """指定パスに .feature ファイルを書き込む。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content), encoding="utf-8")


def minimal_feature(spec_tag: str, scenarios: list[str] | None = None) -> str:
    """最小限の .feature ファイル文字列を生成する。"""
    scenarios = scenarios or ["デフォルトシナリオ"]
    lines = [f"{spec_tag}", f"Feature: {spec_tag} テスト"]
    for name in scenarios:
        lines += [
            f"",
            f"  Scenario: {name}",
            f"    Given テスト前提条件",
            f"    When  テスト実行",
            f"    Then  テスト確認",
        ]
    return "\n".join(lines) + "\n"


# ──────────────────────────────────────────────
# Doorstop プロジェクト作成
# ──────────────────────────────────────────────


def _doorstop_yml(
    prefix: str, sep: str = "-", digits: int = 3, parent: str | None = None
) -> dict:
    """Document .doorstop.yml 設定辞書を返す。"""
    d: dict[str, Any] = {
        "settings": {
            "digits": digits,
            "itemformat": "yaml",
            "prefix": prefix,
            "sep": sep,
        }
    }
    if parent:
        d["settings"]["parent"] = parent
    return d


def _item_dict(
    uid: str,
    header: str = "",
    text: str = "Test item.",
    links: list[str] | None = None,
    testable: bool = True,
    active: bool = True,
    status: str | None = None,
    reviewed: str | None = None,
    cleared: bool | None = None,
    extra: dict | None = None,
) -> dict:
    """Doorstop アイテム YAML 用の辞書を生成する。"""
    num = int(uid.split("-")[1]) if "-" in uid else 1
    # Doorstop YAML リンク形式: [{uid: stamp}, ...]  stamp は None で未スタンプ
    links_data = [{luid: None} for luid in (links or [])]
    d: dict[str, Any] = {
        "active": active,
        "derived": False,
        "header": header.rstrip() + "\n" if header else "\n",
        "level": float(num),
        "links": links_data,
        "normative": True,
        "ref": "",
        "reviewed": reviewed,
        "testable": testable,
        "text": text.rstrip() + "\n" if text else "\n",
    }
    if status:
        d["status"] = status
    if extra:
        d.update(extra)
    return d


def write_doorstop_yaml(items_dir: Path, uid: str, **kwargs) -> Path:
    """1 アイテムの YAML ファイルを items_dir に書き込む。"""
    items_dir.mkdir(parents=True, exist_ok=True)
    data = _item_dict(uid, **kwargs)
    path = items_dir / f"{uid}.yml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=True)
    return path


def _git_init(root: Path) -> None:
    """Doorstop が VCS ルートを検出できるよう、root に git リポジトリを初期化する。"""
    import subprocess

    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", str(root)], capture_output=True, check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "commit",
            "--allow-empty",
            "-m",
            "init",
            "--author",
            "test <test@test.com>",
        ],
        capture_output=True,
    )


def create_doorstop_project_yaml(
    root: Path,
    documents: list[dict],
) -> None:
    """
    YAML ファイルを直接書いて Doorstop プロジェクトを構築する。

    documents: [
        {
          "dir": "reqs",
          "prefix": "REQ",
          "parent": None,
          "items": [
            {"uid": "REQ-001", "header": "...", ...},
          ]
        },
        ...
    ]
    reviewed ハッシュは最後に doorstop API で設定する。
    """
    _git_init(root)

    for doc_config in documents:
        doc_dir = root / doc_config["dir"]
        doc_dir.mkdir(parents=True, exist_ok=True)

        # .doorstop.yml
        dotfile = _doorstop_yml(
            prefix=doc_config["prefix"],
            parent=doc_config.get("parent"),
        )
        with open(doc_dir / ".doorstop.yml", "w", encoding="utf-8") as f:
            yaml.dump(dotfile, f, allow_unicode=True, default_flow_style=False)

        # アイテム YAML
        for item_cfg in doc_config.get("items", []):
            uid = item_cfg["uid"]
            write_doorstop_yaml(
                doc_dir,
                uid,
                header=item_cfg.get("header", "Test"),
                text=item_cfg.get("text", "Test item."),
                links=item_cfg.get("links"),
                testable=item_cfg.get("testable", True),
                active=item_cfg.get("active", True),
                status=item_cfg.get("status"),
                extra=item_cfg.get("extra"),
            )

    # doorstop API で review/clear
    _review_all(root)


def create_doorstop_project_api(
    root: Path,
    req_items: list[dict] | None = None,
    spec_items: list[dict] | None = None,
) -> None:
    """
    Doorstop Python API でプロジェクトを作成し review/clear まで行う。
    UID は順番に自動割り当て: REQ-001, REQ-002, ... / SPEC-001, CORE-001, ...
    """
    import doorstop

    _git_init(root)
    orig = os.getcwd()
    os.chdir(root)
    try:
        tree = doorstop.build()
        req_doc = tree.create_document("reqs", "REQ", sep="-", digits=3)
        spec_doc = tree.create_document(
            "specs", "SPEC", sep="-", digits=3, parent="REQ"
        )

        for cfg in req_items or []:
            item = req_doc.add_item()
            item.header = cfg.get("header", "Test requirement")
            item.text = cfg.get("text", "Test requirement text.")
            item.set("testable", cfg.get("testable", False))
            item.active = cfg.get("active", True)
            if "status" in cfg:
                item.set("status", cfg["status"])
            item.save()

        for cfg in spec_items or []:
            item = spec_doc.add_item()
            item.header = cfg.get("header", "Test specification")
            item.text = cfg.get("text", "Test specification text.")
            item.set("testable", cfg.get("testable", True))
            item.active = cfg.get("active", True)
            if "status" in cfg:
                item.set("status", cfg["status"])
            for link_uid in cfg.get("links", []):
                item.link(link_uid)
            item.save()

    finally:
        os.chdir(orig)

    _review_all(root)


def _review_all(root: Path) -> None:
    """Doorstop ツリーの全アイテムを review/clear して保存する。"""
    import doorstop

    orig = os.getcwd()
    os.chdir(root)
    try:
        tree = doorstop.build()
        # clear (link stamps を更新) → review (fingerprint を設定) の順
        for doc in tree:
            for item in doc:
                try:
                    item.clear()
                except Exception:
                    pass

        for doc in tree:
            for item in doc:
                try:
                    item.review()
                    item.save()
                except Exception:
                    pass
    finally:
        os.chdir(orig)


# ──────────────────────────────────────────────
# 汎用アサーション
# ──────────────────────────────────────────────


def assert_in_output(output: str, expected: str) -> None:
    assert expected in output, (
        f"期待文字列 {expected!r} が出力に見つかりません。\n出力:\n{output}"
    )


def assert_not_in_output(output: str, unexpected: str) -> None:
    assert unexpected not in output, (
        f"不要文字列 {unexpected!r} が出力に含まれています。\n出力:\n{output}"
    )
