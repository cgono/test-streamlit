"""Tests for the LangChain + OpenAI Streamlit app."""

import os
from unittest.mock import MagicMock, patch

import pytest

from app import State, create_graph, get_ai_response


class TestState:
    """Tests for the State TypedDict."""

    def test_state_structure(self):
        """Test that State has the correct structure."""
        state: State = {"messages": []}
        assert "messages" in state
        assert isinstance(state["messages"], list)


class TestCreateGraph:
    """Tests for the create_graph function."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_create_graph_returns_compiled_graph(self):
        """Test that create_graph returns a compiled graph."""
        graph = create_graph()
        assert graph is not None
        assert hasattr(graph, "stream")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_create_graph_has_chatbot_node(self):
        """Test that the graph has the chatbot node configured."""
        graph = create_graph()
        # The graph should be compiled and ready to use
        assert graph is not None


class TestGetAIResponse:
    """Tests for the get_ai_response function."""

    @patch("app.create_graph")
    def test_get_ai_response_returns_string(self, mock_create_graph):
        """Test that get_ai_response returns a string."""
        # Mock the graph and its stream method
        mock_message = MagicMock()
        mock_message.content = "This is a test response"

        mock_graph = MagicMock()
        mock_graph.stream.return_value = [{"messages": [mock_message]}]
        mock_create_graph.return_value = mock_graph

        response = get_ai_response("Hello")
        assert isinstance(response, str)
        assert response == "This is a test response"

    @patch("app.create_graph")
    def test_get_ai_response_handles_empty_events(self, mock_create_graph):
        """Test that get_ai_response handles empty events gracefully."""
        mock_graph = MagicMock()
        mock_graph.stream.return_value = []
        mock_create_graph.return_value = mock_graph

        response = get_ai_response("Hello")
        assert response == ""

    @patch("app.create_graph")
    def test_get_ai_response_calls_graph_with_correct_params(self, mock_create_graph):
        """Test that get_ai_response calls the graph with correct parameters."""
        mock_graph = MagicMock()
        mock_graph.stream.return_value = []
        mock_create_graph.return_value = mock_graph

        get_ai_response("Test prompt")

        mock_graph.stream.assert_called_once_with(
            {"messages": [("user", "Test prompt")]},
            stream_mode="values",
        )

    @patch("app.create_graph")
    def test_get_ai_response_handles_multiple_events(self, mock_create_graph):
        """Test that get_ai_response returns the last message content."""
        # Mock multiple events with messages
        mock_message1 = MagicMock()
        mock_message1.content = "First response"

        mock_message2 = MagicMock()
        mock_message2.content = "Second response"

        mock_graph = MagicMock()
        mock_graph.stream.return_value = [
            {"messages": [mock_message1]},
            {"messages": [mock_message2]},
        ]
        mock_create_graph.return_value = mock_graph

        response = get_ai_response("Hello")
        # Should return the last message
        assert response == "Second response"

    @patch("app.create_graph")
    def test_get_ai_response_propagates_exceptions(self, mock_create_graph):
        """Test that get_ai_response propagates exceptions from the graph."""
        mock_graph = MagicMock()
        mock_graph.stream.side_effect = Exception("API Error")
        mock_create_graph.return_value = mock_graph

        with pytest.raises(Exception, match="API Error"):
            get_ai_response("Hello")


class TestIntegration:
    """Integration tests for the app."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("app.ChatOpenAI")
    def test_full_flow_with_mocked_openai(self, mock_chat_openai):
        """Test the full flow from user input to response."""
        from langchain_core.messages import AIMessage

        # Mock the LLM response with proper AIMessage
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="Mocked AI response")
        mock_chat_openai.return_value = mock_llm

        response = get_ai_response("What is the weather?")

        assert response == "Mocked AI response"
        mock_llm.invoke.assert_called_once()
