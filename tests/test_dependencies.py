import re
from pathlib import Path


def _parse_version_tuple(version_str: str):
    nums = re.findall(r"\d+", version_str)
    return tuple(int(n) for n in nums)


def test_requirements_langchain_modern_versions():
    """Verify requirements.txt specifies LangChain 1.4.9, langchain-core 1.7.6, and all modern partner libraries."""
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
    }
    for pkg, expected_ver in expected_exact.items():
        assert deps.get(pkg) == expected_ver, f"Expected {pkg}{expected_ver}, got {deps.get(pkg)}"

    expected_min = {
        "pymupdf": (1, 25, 0),
        "neo4j": (5, 26, 0),
        "spacy": (3, 8, 4),
    }
    for pkg, min_ver in expected_min.items():
        assert pkg in deps, f"{pkg} dependency missing"
        actual_ver = _parse_version_tuple(deps[pkg])
        assert actual_ver >= min_ver, f"Expected {pkg} >= {min_ver}, got {deps[pkg]}"
