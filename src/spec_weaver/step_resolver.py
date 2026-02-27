# src/spec_weaver/step_resolver.py

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from parse import compile as parse_compile

class StepDefinition:
    def __init__(self, keyword: str, pattern: str, source: str, file: str, line: int):
        self.keyword = keyword.lower()  # 'given', 'when', 'then', 'step'
        self.pattern = pattern
        self.source = source
        self.file = file
        self.line = line
        self._compiled_pattern = parse_compile(pattern)

    def matches(self, keyword: str, text: str) -> bool:
        # keyword matching is loose in behave (step can match any)
        # but usually it's better to match or use 'step'
        if self._compiled_pattern.parse(text) is not None:
            return True
        return False

class StepResolver:
    def __init__(self):
        self.steps: List[StepDefinition] = []

    def load_steps(self, steps_dir: Path):
        """指定ディレクトリ配下の Python ファイルからステップ定義をロードする。"""
        if not steps_dir.exists():
            return

        for py_file in steps_dir.rglob("*.py"):
            self._parse_file(py_file)

    def _parse_file(self, py_file: Path):
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            lines = content.splitlines()

            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        # @given('...'), @when('...'), etc.
                        if isinstance(decorator, ast.Call):
                            func_name = self._get_name(decorator.func)
                            if func_name in ("given", "when", "then", "step"):
                                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                                    pattern = decorator.args[0].value
                                    
                                    # 関数のソースコードを抽出
                                    # node.lineno は 1-indexed
                                    start_line = node.lineno - 1
                                    # デコレータも含めるために少し前に戻る
                                    # 簡単のため、関数の開始行から終了行までを取得
                                    # end_lineno は 3.8+
                                    end_line = getattr(node, "end_lineno", node.lineno + 5)
                                    
                                    # デコレータの行も特定したい
                                    # 実際には ast.get_source_segment があれば楽だが、
                                    # ここでは単純に行番号で切り出す
                                    
                                    # デコレータの開始行を探す
                                    dec_start = decorator.lineno - 1
                                    source_lines = lines[dec_start:end_line]
                                    source = "\n".join(source_lines)
                                    
                                    self.steps.append(StepDefinition(
                                        keyword=func_name,
                                        pattern=pattern,
                                        source=source,
                                        file=str(py_file),
                                        line=node.lineno
                                    ))
        except Exception as e:
            # パースエラーなどは無視（またはログ）
            pass

    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def resolve_step(self, keyword: str, text: str) -> Optional[StepDefinition]:
        """Gherkin ステップに合致する定義を探す。"""
        # keyword は 'Given', 'When', 'Then', 'And', 'But' など
        # 'And', 'But' は呼び出し元で解決されていることを期待するが、
        # ここでは text マッチングを優先する
        
        # マッチングの優先順位: 
        # 1. キーワードが一致するもの
        # 2. 'step' (汎用) デコレータのもの
        # 3. その他
        
        normalized_kw = keyword.lower()
        
        matches = []
        for step in self.steps:
            if step.matches(normalized_kw, text):
                matches.append(step)
        
        if not matches:
            return None
            
        # キーワード一致を優先
        for m in matches:
            if m.keyword == normalized_kw:
                return m
        
        # 'step' を優先
        for m in matches:
            if m.keyword == "step":
                return m
                
        return matches[0]
