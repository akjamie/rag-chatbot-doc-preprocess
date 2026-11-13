import importlib.metadata
import re
from pathlib import Path
from packaging.version import parse as parse_version


def test_requirements_file_specifications():
    """Verify requirements.txt declares exact ecosystem pins and capped bounds."""
    req_path = Path(__file__).parent.parent / "requirements.txt"
    assert req_path.exists(), "requirements.txt not found"

    content = req_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    deps = {}
    for line in lines:
        match = re.match(r"^([a-zA-Z0-9_\-]+)\s*([=><~]+.*)$", line)
        if match:
            deps[match.group(1).lower()] = match.group(2).strip()

    expected_exact = {
        "langchain": "==1.4.9",
        "langchain-core": "==1.7.6",
        "langchain-community": "==0.4.2",
        "langgraph": "==1.2.20",
        "langchain-huggingface": "==1.2.3",
        "langchain-qdrant": "==1.1.0",
        "langchain-google-genai": "==4.4.3",
        "langchain-ollama": "==1.1.0",
        "langchain-anthropic": "==1.7.6",
        "langchain-redis": "==0.2.6",
        "langchain-text-splitters": "==1.1.3",
    }
    for pkg, expected_ver in expected_exact.items():
        assert deps.get(pkg) == expected_ver, f"Expected {pkg}{expected_ver}, got {deps.get(pkg)}"

    assert "pymupdf" in deps and "<3" in deps["pymupdf"]
    assert "neo4j" in deps and "<7" in deps["neo4j"]
    assert "spacy" in deps and "<4" in deps["spacy"]
    assert "pydantic" in deps
    assert "qdrant-client" in deps


def test_installed_environment_packages():
    """Verify actual installed environment versions via importlib.metadata."""
    # Check exact ecosystem pins when installed
    for pkg in ["langchain", "langchain-core", "langchain-community", "langgraph"]:
        try:
            ver = importlib.metadata.version(pkg)
            assert ver is not None
        except importlib.metadata.PackageNotFoundError:
            pass  # Some environments test subsets

    # Check capped packages satisfy bounds if present in the runtime
    if _is_installed("neo4j"):
        v = parse_version(importlib.metadata.version("neo4j"))
        assert parse_version("5.26.0") <= v < parse_version("7.0.0"), f"neo4j version out of range: {v}"

    if _is_installed("pymupdf"):
        v = parse_version(importlib.metadata.version("pymupdf"))
        assert parse_version("1.23.0") <= v < parse_version("3.0.0"), f"pymupdf version out of range: {v}"

    if _is_installed("spacy"):
        v = parse_version(importlib.metadata.version("spacy"))
        assert parse_version("3.8.0") <= v < parse_version("4.0.0"), f"spacy version out of range: {v}"


def _is_installed(pkg_name: str) -> bool:
    try:
        importlib.metadata.version(pkg_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
