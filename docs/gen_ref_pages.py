"""Generate one MkDocs API reference page per package module."""

from pathlib import Path

import mkdocs_gen_files

NAV = mkdocs_gen_files.Nav()
ROOT = Path(__file__).parent.parent
SRC = ROOT / "src" / "python_repo_template"


def main() -> None:
    """Walk the package and write reference markdown pages."""
    for path in sorted(SRC.rglob("*.py")):
        if path.name == "__main__.py":
            continue
        module_path = path.relative_to(SRC.parent).with_suffix("")
        doc_path = path.relative_to(SRC).with_suffix(".md")
        full_doc_path = Path("reference", doc_path)
        parts = tuple(module_path.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = Path("reference", doc_path)
        NAV[parts] = doc_path.as_posix()
        with mkdocs_gen_files.open(full_doc_path, "w") as fd:
            identifier = ".".join(parts)
            fd.write(f"# `{identifier}`\n\n::: {identifier}\n")
        mkdocs_gen_files.set_edit_path(
            full_doc_path,
            Path("..") / path.relative_to(ROOT),
        )

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(NAV.build_literate_nav())


main()
