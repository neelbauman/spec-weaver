import re
from pathlib import Path

file_path = Path("specification/features/steps/step_trace.py")
content = file_path.read_text()

replacements = [
    (
        r"@given\('以下のREQアイテムが存在する:'\)\s*# type: ignore\ndef given_28140be4\(context\):[\s\S]*?raise NotImplementedError\('STEP: 以下のREQアイテムが存在する:'\)",
        """@given('以下のREQアイテムが存在する:')  # type: ignore\ndef given_28140be4(context):\n    \"\"\"以下のREQアイテムが存在する:\"\"\"\n    from specification.features.steps._helpers import write_doorstop_yaml\n    for row in context.table:\n        write_doorstop_yaml(context.temp_dir / "reqs", row["ID"], header=row.get("Header", ""))\n"""
    ),
    (
        r"@given\('以下のfeatureファイルが存在する:'\)\s*# type: ignore\ndef given_a838a6ff\(context\):[\s\S]*?raise NotImplementedError\('STEP: 以下のfeatureファイルが存在する:'\)",
        """@given('以下のfeatureファイルが存在する:')  # type: ignore\ndef given_a838a6ff(context):\n    \"\"\"以下のfeatureファイルが存在する:\"\"\"\n    features_dir = context.temp_dir / "specification" / "features"\n    features_dir.mkdir(parents=True, exist_ok=True)\n    for row in context.table:\n        filename = row["File"]\n        tags = row.get("Tags", "")\n        path = features_dir / filename\n        path.write_text(f"{tags}\\nFeature: Test Feature\\n")\n"""
    ),
    (
        r"@when\('`spec-weaver trace (.+?)` を実行する'\)\s*# type: ignore\ndef when_([0-9a-f]+)\(context\):[\s\S]*?raise NotImplementedError\('STEP: `spec-weaver trace (.+?)` を実行する'\)",
        """@when('`spec-weaver trace {param0}` を実行する')  # type: ignore\ndef when_\\2(context, param0):\n    \"\"\"`spec-weaver trace {param0}` を実行する\"\"\"\n    import shlex\n    from specification.features.steps._helpers import run_spec_weaver\n    args = shlex.split(f"trace {param0}")\n    for i, arg in enumerate(args):\n        if arg == "./specification/features":\n            args[i] = str(context.temp_dir / "specification" / "features")\n        elif arg == "./nonexistent/features":\n            args[i] = str(context.temp_dir / "nonexistent" / "features")\n    context.result = run_spec_weaver(args, cwd=context.temp_dir)\n"""
    )
]

for old, new in replacements:
    content = re.sub(old, new, content)

file_path.write_text(content)
