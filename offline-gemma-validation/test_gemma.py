from gemma_client import GemmaClient


def test_gemma_response():
    client = GemmaClient()

    response = client.generate(
        "What is supervised learning? Answer in one sentence."
    )

    assert response
    assert isinstance(response, str)
    assert len(response.strip()) > 0


if __name__ == "__main__":
    test_gemma_response()
    print("Gemma offline validation test passed.")