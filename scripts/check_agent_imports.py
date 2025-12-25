import langchain.agents as agents
import inspect
import pkgutil
from importlib import import_module

def list_public_members(module):
    return sorted(
        name
        for name in dir(module)
        if not name.startswith("_")
    )

print("=== Top-level in langchain.agents ===")
print(list_public_members(agents))

print("\n=== Submodules under langchain.agents ===")
submods = [
    m.name
    for m in pkgutil.iter_modules(agents.__path__, agents.__name__ + ".")
]
for mod_name in sorted(submods):
    print(f"\n[{mod_name}]")
    mod = import_module(mod_name)
    print(list_public_members(mod))
