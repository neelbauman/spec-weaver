import os
import subprocess
import doorstop
import re

def run_cli(context, args):
    cmd = ["spec-weaver"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=context.temp_dir
    )
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.exit_code = result.returncode
    return result

def setup_doorstop(context, prefixes=["SPEC"]):
    # Initialize features dir
    os.makedirs(os.path.join(context.temp_dir, "features"), exist_ok=True)
    
    last_prefix = None
    for prefix in prefixes:
        doc_dir = prefix.lower() + "s"
        cmd = ["doorstop", "create", prefix, doc_dir]
        if last_prefix:
            cmd += ["--parent", last_prefix]
        
        res = subprocess.run(cmd, cwd=context.temp_dir, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"STDOUT: {res.stdout}")
            print(f"STDERR: {res.stderr}")
            res.check_returncode()
        
        # Set sep: '-' in .doorstop.yml
        doorstop_yml = os.path.join(context.temp_dir, doc_dir, ".doorstop.yml")
        with open(doorstop_yml, "r") as f:
            content = f.read()
        
        if "sep: ''" in content:
            content = content.replace("sep: ''", "sep: '-'")
        elif "sep:" in content:
            content = re.sub(r"sep:.*", "sep: '-'", content)
        else:
            if "settings:" in content:
                content = content.replace("settings:", "settings:\n  sep: '-'")
            else:
                content += "\nsettings:\n  sep: '-'\n"
        
        with open(doorstop_yml, "w") as f:
            f.write(content)
        last_prefix = prefix
    
    return doorstop.build(context.temp_dir)

def create_feature_file(context, filename, content):
    feature_dir = os.path.join(context.temp_dir, "features")
    os.makedirs(feature_dir, exist_ok=True)
    path = os.path.join(feature_dir, filename)
    # Fix potential double escaping from strings
    content = content.replace("\\n", "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
