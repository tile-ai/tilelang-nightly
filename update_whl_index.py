import hashlib
import pathlib
import re
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="nightly")
args = parser.parse_args()
base_url = "https://github.com/tile-ai/tilelang-nightly/releases/download"
pattern = re.compile(
    r"tilelang-"
    r"((\d+\.)+\d+(?:\.post\d+)?)"
    r"(?:\+([a-f0-9]+))?"        
    r".*?\.cu(\d+)"                
)
base_path = "tilelang-whl/nightly"
vvver = " Nightly"
star = "*"

if args.mode != "nightly":
    vvver = ""
    base_path = "tilelang-whl"
    base_url = "https://github.com/tile-ai/tilelang/releases/download"
    star = "cu*"
if args.mode == "nightly":
    with (pathlib.Path(base_path) / "index.html").open("w") as f:
        f.write(
            """<!DOCTYPE html>
<h1>TileLang Nightly Python Wheels</h1>\n"""
        )
for index_dir in pathlib.Path(base_path).glob(star):
    if index_dir.is_dir():
        os.system(f"rm -rf {index_dir}")
dir_set = set()
for path in sorted(pathlib.Path("dist").glob("*.whl")):
        with open(path, "rb") as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()
        match = pattern.search(path.name)
        if match:
            base_version = match.group(1)
            commit_hash = match.group(3) or "" 
            cuda_version = match.group(4)  

            full_version = base_version
            if commit_hash:
                full_version += "+" + commit_hash

        else:
            continue
        index_dir = pathlib.Path(f"{base_path}/cu{cuda_version}")
        index_dir.mkdir(exist_ok=True)
        ver = full_version.replace("+", "%2B")
        if args.mode != "nightly":
            ver = 'v' + ver
        full_url = f"{base_url}/{ver}/{path.name}#sha256={sha256}"
        if cuda_version not in dir_set:
            with (index_dir / "index.html").open("w") as f:
                f.write(
                    f"""<!DOCTYPE html>
    <h1>TileLang{vvver} Python Wheels for CUDA {cuda_version}</h1>\n"""
                )
            dir_set.add(cuda_version)
        with (index_dir / "index.html").open("a") as f:
            f.write(f'<a href="{full_url}">{path.name}</a><br>\n')
    
with (pathlib.Path(base_path) / "index.html").open("a+") as f:
    f.write(
        f'<a href="cu{cuda_version}/">cu{cuda_version}</a><br>'
    )

dir_list = []

for index_dir in pathlib.Path("tilelang-whl").iterdir():
    if index_dir.is_dir():
        if index_dir.name[0] != '.':
            dir_list.append(index_dir.name)
dir_list.sort()
with open("tilelang-whl/index.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<h1>TileLang Python Wheels</h1>\n"""
    )
for dir_name in dir_list:
    with open("tilelang-whl/index.html", "a") as f:
        f.write(f'<a href="{dir_name}/">{dir_name}</a><br>\n')   
