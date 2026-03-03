import doorstop
import json

tree = doorstop.build()
data = []
for document in tree:
    for item in document:
        if item.active and item.get('testable'):
            gherkin_files = list(item.get('gherkin_fingerprints', {}).keys()) if isinstance(item.get('gherkin_fingerprints'), dict) else []
            # Wait, gherkin_fingerprints is usually a list of dicts: "- ./specification/features/audit.feature: | hash"
            if isinstance(item.get('gherkin_fingerprints'), list):
                files = []
                for entry in item.get('gherkin_fingerprints'):
                    if isinstance(entry, dict):
                        files.extend(list(entry.keys()))
                gherkin_files = files
            data.append({
                'uid': str(item.uid),
                'path': str(item.path),
                'features': gherkin_files
            })
print(json.dumps(data, indent=2))
