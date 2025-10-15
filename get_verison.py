import pathlib
import re

pattern = re.compile(
    r"tilelang-"
    r"((\d+\.)+\d+(?:\.post\d+)?)"
    r"\+cu(\d+)\." 
    r"git([a-z0-9]+)?"                       
)

path = next(pathlib.Path("dist").glob("*.whl"))
match = pattern.search(path.name)
cuda_version_ = None
if match:
    base_version = match.group(1)
    commit_hash = match.group(4) or "" 
    cuda_version_ = match.group(3)  
    full_version = base_version
    if commit_hash:
        full_version += "+" + commit_hash
print(full_version, end="")