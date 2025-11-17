import os
from typing import Annotated, TypedDict

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

# Load environment variables
load_dotenv()


# Define the state schema for our graph
class State(TypedDict):
    """State schema for the LangChain graph."""

    messages: Annotated[list, add_messages]


# Initialize the LangChain graph
def create_graph():
    """Create and compile the LangChain graph with OpenAI."""
    # Initialize the ChatOpenAI model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # Define the chatbot node
    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    # Create the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_edge(START, "chatbot")

    # Compile and return the graph
    return graph_builder.compile()


def get_ai_response(prompt: str) -> str:
    """Get AI response for the given prompt using LangChain graph.

    Args:
        prompt: User input text

    Returns:
        AI response content

    Raises:
        Exception: If there's an error communicating with OpenAI
    """
    graph = create_graph()
    events = graph.stream(
        {"messages": [("user", prompt)]},
        stream_mode="values",
    )

    response_content = ""
    for event in events:
        if "messages" in event and event["messages"]:
            last_message = event["messages"][-1]
            if hasattr(last_message, "content"):
                response_content = last_message.content

    return response_content


def display_chat_history():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def show_api_key_warning():
    """Display warning when API key is not configured."""
    st.warning("⚠️ OpenAI API key not found! Please set the OPENAI_API_KEY environment variable.")
    st.info("Create a `.env` file in the project root with: `OPENAI_API_KEY=your-api-key-here`")


def handle_user_input(prompt: str):
    """Process user input and get AI response.

    Args:
        prompt: User input text
    """
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_content = get_ai_response(prompt)
                st.markdown(response_content)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_content})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure your OpenAI API key is valid and you have credits.")


def main():
    """Main application function."""
    # Streamlit UI
    st.title("LangChain + OpenAI Chat Interface")
    st.write("Ask me anything! This app uses LangChain with OpenAI's API.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    display_chat_history()

    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        show_api_key_warning()
        return

    # Handle chat input
    prompt = st.chat_input("What would you like to know?")
    if prompt:
        handle_user_input(prompt)

    # Add a clear chat button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
