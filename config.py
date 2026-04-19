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
    def _get_key(*env_names) -> str | None:
        for name in env_names:
            val = os.environ.get(name)
            if val:
                return val
        return None

    @staticmethod
    def has_any_api_key() -> bool:
        """Check if at least one judge API key is configured."""
        return bool(
            Settings._get_key("OPENAI_API_KEY", "GPT_API_KEY")
            or Settings._get_key("ANTHROPIC_API_KEY", "CLAUDE_API_KEY")
            or Settings._get_key("GOOGLE_API_KEY", "GEMINI_API_KEY")
        )

    @staticmethod
    def available_judges() -> list[str]:
        """List which judge providers have API keys configured."""
        judges = []
        if Settings._get_key("OPENAI_API_KEY", "GPT_API_KEY"):
            judges.append("OpenAI (GPT-4o)")
        if Settings._get_key("ANTHROPIC_API_KEY", "CLAUDE_API_KEY"):
            judges.append("Anthropic (Claude)")
        if Settings._get_key("GOOGLE_API_KEY", "GEMINI_API_KEY"):
            judges.append("Google (Gemini)")
        return judges


settings = Settings()
