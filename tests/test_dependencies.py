import re
from pathlib import Path


def test_requirements_langchain_modern_versions():
    """Verify requirements.txt specifies LangChain 1.4.9, langchain-core 1.7.6, and modern libraries."""
    req_path = Path(__file__).parent.parent / "requirements.txt"
    assert req_path.exists(), "requirements.txt not found"

    content = req_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    deps = {}
    for line in lines:
        match = re.match(r"^([a-zA-Z0-9_\-]+)\s*([=><~]+.*)$", line)
        if match:
            deps[match.group(1).lower()] = match.group(2).strip()

    assert deps.get("langchain") == "==1.4.9", f"Expected langchain==1.4.9, got {deps.get('langchain')}"
    assert deps.get("langchain-core") == "==1.7.6", f"Expected langchain-core==1.7.6, got {deps.get('langchain-core')}"
    assert deps.get("langchain-community") == "==0.4.2", f"Expected langchain-community==0.4.2, got {deps.get('langchain-community')}"
    assert deps.get("langchain-huggingface") == "==1.2.3", f"Expected langchain-huggingface==1.2.3, got {deps.get('langchain-huggingface')}"
    assert "pymupdf" in deps, "pymupdf dependency missing"
    assert "neo4j" in deps, "neo4j dependency missing"

