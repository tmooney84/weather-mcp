def create_provider():

    provider = os.getenv(
        "LLM_PROVIDER",
        "ollama"
    )

    if provider == "ollama":

        return OllamaProvider(
            model=os.getenv(
                "OLLAMA_MODEL",
                "granite4.0-h-tiny"
            )
        )
    
    elif provider == "anthropic":

        return AnthropicProvider()
    
    else:

        raise ValueError(
            f"Unknown provider: {provider}"
        )