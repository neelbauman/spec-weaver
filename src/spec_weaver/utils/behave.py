
import subprocess
import shutil
import re
from pathlib import Path
from typing import List, Tuple, Optional

def check_behave_steps(features_dir: Path) -> Tuple[List[str], List[str]]:
    """
    behave --dry-run -f steps.usage を実行し、
    未使用のステップ定義 (unused) と未定義のステップ (undefined) を抽出します。
    """
    if shutil.which("behave") is None:
        # behave が見つからない場合は空リストを返す（警告は呼び出し側で行う）
        return [], []

    # uv run behave ... を試みる (uv 環境を優先)
    cmd = ["behave", str(features_dir), "--dry-run", "-f", "steps.usage"]
    if shutil.which("uv") is not None:
        cmd = ["uv", "run"] + cmd

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
    except Exception:
        return [], []

    return parse_behave_usage(result.stdout)

def parse_behave_usage(output: str) -> Tuple[List[str], List[str]]:
    """
    behave --dry-run -f steps.usage の出力をパースします。
    """
    unused_defs = []
    undefined_steps = []
    
    lines = output.splitlines()
    current_section = None
    
    for line in lines:
        if "UNUSED STEP DEFINITIONS" in line:
            current_section = "unused"
            continue
        elif "UNDEFINED STEPS" in line:
            current_section = "undefined"
            continue
        
        # セクション内の項目は通常 2 スペースでインデントされている
        if current_section == "unused":
            if line.startswith("  "):
                unused_defs.append(line.strip())
            elif line.strip() == "":
                continue
            else:
                current_section = None
        elif current_section == "undefined":
            if line.startswith("  "):
                undefined_steps.append(line.strip())
            elif line.strip() == "":
                continue
            else:
                current_section = None
                
    return unused_defs, undefined_steps
