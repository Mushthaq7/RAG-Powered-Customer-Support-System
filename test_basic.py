"""
Basic tests for the Intercom AI Support system
"""
import pytest
import asyncio
from app.config import settings
from app.ai import AIService
from app.intercom import IntercomClient
from app.utils import sanitize_message, categorize_urgency


def test_config_loading():
    """Test that configuration loads correctly"""
    assert hasattr(settings, 'APP_NAME')
    assert settings.APP_NAME == "Intercom AI Support"


def test_sanitize_message():
    """Test message sanitization"""
    # Test normal message
    assert sanitize_message("Hello world") == "Hello world"

    # Test message with HTML
    assert sanitize_message(
        "<script>alert('xss')</script>") == "scriptalert(xss)/script"

    # Test empty message
    assert sanitize_message("") == ""

    # Test None message
    assert sanitize_message(None) == ""


def test_categorize_urgency():
    """Test urgency categorization"""
    assert categorize_urgency("This is an emergency!") == "critical"
    assert categorize_urgency("I need help with this issue") == "high"
    assert categorize_urgency("How do I do this?") == "medium"
    assert categorize_urgency("Just saying hello") == "low"


def test_ai_service_initialization():
    """Test AI service can be initialized"""
    try:
        ai_service = AIService()
        assert ai_service is not None
        assert hasattr(ai_service, 'generate_response')
    except Exception as e:
        # This might fail if OpenAI API key is not set, which is expected
        assert "OPENAI_API_KEY" in str(e) or "INTERCOM_ACCESS_TOKEN" in str(e)


def test_intercom_client_initialization():
    """Test Intercom client can be initialized"""
    try:
        client = IntercomClient()
        assert client is not None
        assert hasattr(client, 'reply_to_conversation')
    except Exception as e:
        # This might fail if Intercom token is not set, which is expected
        assert "INTERCOM_ACCESS_TOKEN" in str(e)


if __name__ == "__main__":
    # Run basic tests
    test_config_loading()
    test_sanitize_message()
    test_categorize_urgency()
    print("All basic tests passed!")
