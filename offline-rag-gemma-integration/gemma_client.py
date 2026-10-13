import importlib.util
from pathlib import Path


# Load the previously validated Gemma client directly from its file.
GEMMA_FILE = (
    Path(__file__).resolve().parent.parent
    / "offline-gemma-validation"
    / "gemma_client.py"
)


def load_validated_gemma_client():
    """Load the validated Gemma client without a module-name collision."""

    spec = importlib.util.spec_from_file_location(
        "validated_gemma_client",
        GEMMA_FILE,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load Gemma client from: {GEMMA_FILE}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.GemmaClient


ValidatedGemmaClient = load_validated_gemma_client()


class GemmaClient:
    """
    Integration adapter for the locally validated Gemma client.

    Uses Ollama and Gemma locally. No cloud API is required.
    """

    def __init__(self, model: str = "gemma3:1b"):
        self.client = ValidatedGemmaClient(model=model)

    def generate(self, prompt: str) -> str:
        """Send a grounded prompt to the local Gemma model."""

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        return self.client.generate(prompt)


if __name__ == "__main__":
    client = GemmaClient()

    response = client.generate(
        "Explain supervised learning in one simple sentence."
    )

    print("Gemma integration test:")
    print(response)