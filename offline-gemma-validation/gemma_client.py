import ollama


class GemmaClient:
    """Client for communicating with the locally running Gemma model."""

    def __init__(self, model: str = "gemma3:1b"):
        self.model = model

    def generate(self, prompt: str) -> str:
        """Send a prompt to the local Gemma model and return its response."""
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]


if __name__ == "__main__":
    client = GemmaClient()

    prompt = "Explain machine learning in one sentence."

    response = client.generate(prompt)

    print("Gemma response:")
    print(response)