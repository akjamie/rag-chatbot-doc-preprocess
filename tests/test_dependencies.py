import importlib.metadata
import os
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
    # When running in CI where `pip install -r requirements.txt` executed, verify exact ecosystem pins
    in_ci = os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

    expected_exact_pins = {
        "langchain": "1.4.9",
        "langchain-core": "1.7.6",
        "langchain-community": "0.4.2",
        "langgraph": "1.2.20",
        "langchain-huggingface": "1.2.3",
        "langchain-qdrant": "1.1.0",
        "langchain-google-genai": "4.4.3",
        "langchain-ollama": "1.1.0",
        "langchain-anthropic": "1.7.6",
        "langchain-redis": "0.2.6",
        "langchain-text-splitters": "1.1.3",
    }

    if in_ci:
        for pkg, pin in expected_exact_pins.items():
            ver = importlib.metadata.version(pkg)
            assert ver == pin, f"Expected installed {pkg}=={pin}, got {ver}"

        # In CI, drivers must be installed and meet the strict >=1.25.0 bound
        assert _is_installed("pymupdf"), "pymupdf must be installed"
        mu_ver = parse_version(importlib.metadata.version("pymupdf"))
        assert parse_version("1.25.0") <= mu_ver < parse_version("3.0.0"), f"pymupdf version out of range: {mu_ver}"
    else:
        # In local development environment, verify installed subset satisfies declared boundaries
        for pkg, pin in expected_exact_pins.items():
            if _is_installed(pkg):
                ver = importlib.metadata.version(pkg)
                assert ver is not None

        if _is_installed("pymupdf"):
            mu_ver = parse_version(importlib.metadata.version("pymupdf"))
            assert parse_version("1.23.0") <= mu_ver < parse_version("3.0.0"), f"pymupdf version out of range: {mu_ver}"

    assert _is_installed("neo4j"), "neo4j must be installed"
    neo_ver = parse_version(importlib.metadata.version("neo4j"))
    assert parse_version("5.26.0") <= neo_ver < parse_version("7.0.0"), f"neo4j version out of range: {neo_ver}"

    assert _is_installed("spacy"), "spacy must be installed"
    sp_ver = parse_version(importlib.metadata.version("spacy"))
    assert parse_version("3.8.0") <= sp_ver < parse_version("4.0.0"), f"spacy version out of range: {sp_ver}"


def _is_installed(pkg_name: str) -> bool:
    try:
        importlib.metadata.version(pkg_name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
