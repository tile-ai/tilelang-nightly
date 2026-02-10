import pathlib
import re
from datetime import datetime

pattern = re.compile(
    r"tilelang-"
    r"((\d+\.)+\d+(?:\.post\d+)?)"                   
)

path = next(pathlib.Path("dist").glob("*.whl"))
match = pattern.search(path.name)
cuda_version_ = None
if match:
    base_version = match.group(1)
print("v" + base_version + datetime.now().strftime("+%Y%m%d"), end="")
