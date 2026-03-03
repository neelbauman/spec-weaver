import re
from pathlib import Path

# --- Fix step_trace.py ---
trace_file = Path("specification/features/steps/step_trace.py")
trace_content = trace_file.read_text()

trace_content = trace_content.replace("""@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    \"\"\"Doorstopツリーが初期化されている

    Scenarios:
      - 
    \"\"\"
    pass""", """@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    \"\"\"Doorstopツリーが初期化されている\"\"\"
    create_doorstop_project_api(context.temp_dir)
    context.repo_root = context.temp_dir
""")

trace_content = trace_content.replace("""@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    \"\"\"以下のSPECアイテムが存在する:

    Scenarios:
      - 
    \"\"\"
    pass""", """@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    \"\"\"以下のSPECアイテムが存在する:\"\"\"
    from specification.features.steps._helpers import write_doorstop_yaml
    import json
    for row in context.table:
        extra = {}
        if "impl_files" in row.headings and row["impl_files"]:
            try:
                extra["impl_files"] = json.loads(row["impl_files"])
            except json.JSONDecodeError:
                extra["impl_files"] = row["impl_files"]
        write_doorstop_yaml(context.temp_dir / "specs", row["ID"], header=row.get("Header", ""), extra=extra)
""")

trace_file.write_text(trace_content)
