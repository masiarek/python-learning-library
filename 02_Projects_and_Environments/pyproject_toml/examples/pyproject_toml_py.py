#!/usr/bin/env python3
"""pyproject.toml is one file with several audiences -- and Python can read it.

Everything below parses the same embedded document. Nothing is read from disk,
so this program prints the same thing on every machine.
"""

import io
import tomllib

# A small but real pyproject.toml: a project that declares itself, pins its
# docs toolchain in a group, and owns a second package in the same repository.
PYPROJECT = """\
[project]
name = "star-voting-library"
version = "0.1.0"
requires-python = ">=3.10,<3.14"
dependencies = [
    "pref-voting>=1.18",
    "pyyaml>=6.0.3",
]

[project.optional-dependencies]
plotting = ["matplotlib>=3.8"]

[dependency-groups]
dev = ["pytest>=8.0", "mypy>=2.0.0"]
docs = ["mkdocs-material>=9.5", "mkdocs-same-dir==0.1.3"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.uv.workspace]
members = ["engine"]

[tool.uv.sources]
starvote = { workspace = true, editable = true }
"""

data = tomllib.loads(PYPROJECT)


def rule(n, title):
    print(f"\n{n}. {title}")


print("READING pyproject.toml WITH THE STANDARD LIBRARY")
print("tomllib has shipped with Python since 3.11. No install, no dependency.")

rule(1, "THE FILE HAS TWO KINDS OF TABLE, AND ONLY ONE IS STANDARDISED")
OWNERS = {
    "project": "standard, PEP 621 -- every tool reads it the same way",
    "dependency-groups": "standard, PEP 735 -- same, and it is the newest one",
    "tool": "each tool's own room, and nobody else looks inside",
}
for key in data:
    print(f"     [{key}]".ljust(26) + OWNERS[key])
print()
print("     Anything under [tool.X] belongs to X alone: [tool.pytest] is not")
print("     part of the packaging standard and pytest is the only reader.")
print("     That is the whole convention -- one file, one room per tool.")

rule(2, "WHAT THE PROJECT SAYS ABOUT ITSELF")
project = data["project"]
for field in ("name", "version", "requires-python"):
    print(f"     {field:<16} {project[field]!r}")
print(f"     {'dependencies':<16} {len(project['dependencies'])} of them:")
for dep in project["dependencies"]:
    print(f"                      {dep}")

rule(3, "A NESTED TABLE IS JUST A NESTED DICT")
print("     A dotted header is nothing but nesting: the table [tool.uv.workspace]")
print("     is three dict lookups, and a key inside it is a fourth.")
print()
print(f"     data['tool']['uv']['workspace']            ->  "
      f"{data['tool']['uv']['workspace']}")
print(f"     data['tool']['uv']['workspace']['members'] ->  "
      f"{data['tool']['uv']['workspace']['members']}")
print(f"     data['tool']['uv']['sources']              ->  "
      f"{data['tool']['uv']['sources']}")
print(f"     data['tool']['pytest']['ini_options']      ->  "
      f"{data['tool']['pytest']['ini_options']}")
print()
print("     Those two uv tables are the whole of a WORKSPACE. 'members' says")
print("     this repository holds other packages, each with its own")
print("     pyproject.toml, that share one resolved environment. 'sources'")
print("     says the name starvote resolves to the copy in this repository")
print("     and not to the one on PyPI -- editable, so an edit is live.")
print()
print("     That is what an editor offers to read when it proposes deriving")
print("     the project layout from pyproject.toml: the answer is in the")
print("     file, so it no longer has to guess which folders are packages.")

rule(4, "THREE THINGS ARE CALLED DEPENDENCIES AND THEY ARE NOT THE SAME")
print("     [project].dependencies")
print("       who needs them: a USER of this code, always, on install")
for dep in data["project"]["dependencies"]:
    print(f"         {dep}")
print()
print("     [project.optional-dependencies]")
print("       who needs them: a USER who asks -- pip install 'star-voting-library[plotting]'")
for extra, deps in data["project"]["optional-dependencies"].items():
    print(f"         {extra:<9} {', '.join(deps)}")
print()
print("     [dependency-groups]")
print("       who needs them: a DEVELOPER of this code, and nobody else ever")
for group, deps in data["dependency-groups"].items():
    print(f"         {group:<9} {', '.join(deps)}")
print()
print("     Only the third one is invisible to whoever installs the package.")
print("     pytest is not a dependency of the library; it is a dependency of")
print("     working on the library, and PEP 735 exists to say so in the file")
print("     rather than in a requirements-dev.txt nothing validates.")

rule(5, "THE VALUES ARRIVE AS PYTHON TYPES, AND THE QUOTES DECIDE WHICH")
samples = ['v = "1.10"', "v = 1.10", "v = true", "v = 2026-09-06", 'v = ["a", "b"]']
for src in samples:
    value = tomllib.loads(src)["v"]
    print(f"     {src:<18} ->  {value!r:<28} {type(value).__name__}")
print()
print("     No bare word is a boolean: TOML has only true and false, lower")
print("     case. There is nothing here for a Yes or an Off to be coerced")
print("     into, which is the one thing TOML buys over YAML for a config file.")

rule(6, "tomllib WANTS BYTES -- THIS IS CHAPTER 1 AGAIN")
print("     TOML is DEFINED to be UTF-8, so tomllib decodes the bytes itself")
print("     rather than trusting whatever open() would have guessed.")
print()
# The third case's message is NOT printed: CPython reworded it in 3.14, and an
# answer key that shows it would pass on one interpreter and fail on another.
CASES = (
    ("tomllib.load(binary_file)", lambda: tomllib.load(io.BytesIO(PYPROJECT.encode())), True),
    ("tomllib.loads(str)", lambda: tomllib.loads(PYPROJECT), True),
    ("tomllib.load(text_file)", lambda: tomllib.load(io.StringIO(PYPROJECT)), True),
    ("tomllib.loads(bytes)", lambda: tomllib.loads(PYPROJECT.encode()), False),
)
for label, call, show_message in CASES:
    try:
        result = call()
    except TypeError as exc:
        detail = str(exc) if show_message else "(message deliberately not shown -- see below)"
        print(f"     {label:<26} {type(exc).__name__}")
        print(f"     {'':<26}   {detail}")
    else:
        print(f"     {label:<26} OK -- {len(result)} top-level tables")
print()
print("     load() takes a file opened 'rb'; loads() takes a str. Getting it")
print("     backwards is a TypeError, not a mojibake bug -- which is the point")
print("     of refusing to guess.")
print()
print("     The last message is withheld because it is not stable. Up to 3.13")
print("     the bytes reached str.replace() and CPython reported that; 3.14")
print("     catches it and says so in tomllib's own words. Same type, same")
print("     bug, different sentence. AN EXCEPTION MESSAGE IS NOT API: catch")
print("     the type, and never match on the text.")

rule(7, "IT ONLY READS")
print("     There is no tomllib.dump(). Writing TOML is not in the standard")
print("     library, on purpose: reading config is everyone's problem, and")
print("     writing it -- preserving comments and layout -- is a hard one.")
print("     Edit pyproject.toml by hand, or let your tool do it.")
