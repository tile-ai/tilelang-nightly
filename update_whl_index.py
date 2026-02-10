import hashlib
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="nightly")
args = parser.parse_args()
base_url = "https://github.com/tile-ai/tilelang-nightly/releases/download"
base_path = "tilelang-whl/nightly"
vvver = " Nightly"

if args.mode != "nightly":
    vvver = ""
    base_path = "tilelang-whl"
    base_url = "https://github.com/tile-ai/tilelang/releases/download"

index_dir = pathlib.Path(base_path)
index_dir.mkdir(parents=True, exist_ok=True)

with (index_dir / "index.html").open("w") as f:
    f.write(
        f"""<!DOCTYPE html>
<h1>TileLang{vvver} Python Wheels</h1>\n"""
    )

for path in sorted(pathlib.Path("dist").glob("*.whl")):
    with open(path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    with open("version", "r") as f:
        full_version = f.read()

    ver = full_version.replace("+", "%2B")
    if args.mode != "nightly":
        ver = 'v' + ver
    full_url = f"{base_url}/{ver}/{path.name}#sha256={sha256}"
    with (index_dir / "index.html").open("a") as f:
        f.write(f'<a href="{full_url}">{path.name}</a><br>\n')
    break

if args.mode == "nightly":
    dir_list = []
    for d in pathlib.Path("tilelang-whl").iterdir():
        if d.is_dir() and not d.name.startswith('.'):
            dir_list.append(d.name)
    dir_list.sort()
    with (pathlib.Path("tilelang-whl") / "index.html").open("w") as f:
        f.write(
            """<!DOCTYPE html>
<h1>TileLang Python Wheels</h1>\n"""
        )
    for dir_name in dir_list:
        with (pathlib.Path("tilelang-whl") / "index.html").open("a") as f:
            f.write(f'<a href="{dir_name}/">{dir_name}</a><br>\n')   
