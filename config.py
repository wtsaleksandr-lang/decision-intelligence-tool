"""
Decision Intelligence Tool — Configuration.
"""

import os


class Settings:
    """Application settings loaded from environment."""

    # Server
    host: str = "0.0.0.0"
    port: int = int(os.environ.get("PORT", "8000"))
    debug: bool = os.environ.get("DEBUG", "").lower() == "true"

    # Cost profile: cheap | balanced | full
    cost_profile: str = os.environ.get("COST_PROFILE", "cheap")

    # Limits
    max_options: int = 10
    min_options: int = 2
    max_criteria: int = 10
    judge_timeout: int = 300

    @staticmethod
    def has_any_api_key() -> bool:
        """Check if at least one judge API key is configured."""
        keys = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]
        return any(os.environ.get(k) for k in keys)

    @staticmethod
    def available_judges() -> list[str]:
        """List which judge providers have API keys configured."""
        judges = []
        if os.environ.get("OPENAI_API_KEY"):
            judges.append("OpenAI (GPT-4o)")
        if os.environ.get("ANTHROPIC_API_KEY"):
            judges.append("Anthropic (Claude)")
        if os.environ.get("GOOGLE_API_KEY"):
            judges.append("Google (Gemini)")
        return judges


settings = Settings()
