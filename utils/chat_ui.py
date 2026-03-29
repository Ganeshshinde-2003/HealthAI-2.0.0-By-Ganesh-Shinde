"""
HealthAI Chat UI Component

Floating chat widget in bottom-right corner with popup chat window.
Beautiful, responsive design with smooth animations.

Version: 2.0.0
Author: Ganesh Shinde
"""

import streamlit as st
from typing import Optional
from .chat_agent import HealthChatAgent


def render_chat_interface():
    """Render the complete floating chat interface."""

    # Initialize chat agent if not exists
    if 'chat_agent' not in st.session_state:
        st.session_state.chat_agent = HealthChatAgent()
        st.session_state.chat_agent.initialize_context()

    # Initialize chat open state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False

    # Inject CSS for floating chat
    _inject_floating_chat_styles()

    # Render floating chat bubble and window
    _render_floating_chat()

    # Open dialog when chat is toggled
    if st.session_state.chat_open:
        _render_chat_dialog()


def _inject_floating_chat_styles():
    """Inject CSS for floating chat widget."""

    st.markdown("""
    <style>
    /* Floating chat bubble button */
    .floating-chat-bubble {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: pulse-shadow 2s infinite;
    }

    .floating-chat-bubble:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.7);
    }

    .floating-chat-bubble svg {
        width: 30px;
        height: 30px;
        fill: white;
    }

    @keyframes pulse-shadow {
        0%, 100% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 4px 30px rgba(102, 126, 234, 0.8); }
    }

    /* Floating chat window */
    .floating-chat-window {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 400px;
        max-width: calc(100vw - 60px);
        height: 600px;
        max-height: calc(100vh - 150px);
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        z-index: 999998;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: slideUp 0.3s ease-out;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Chat window header */
    .chat-window-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 20px;
        font-weight: 600;
        font-size: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .chat-window-close {
        cursor: pointer;
        font-size: 20px;
        line-height: 1;
        padding: 4px 8px;
        border-radius: 4px;
        transition: background 0.2s;
    }

    .chat-window-close:hover {
        background: rgba(255, 255, 255, 0.2);
    }

    /* Hide the Streamlit chat elements when in floating mode */
    .floating-chat-window .stChatFloatingInputContainer {
        background: white !important;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .floating-chat-window {
            width: calc(100vw - 20px);
            right: 10px;
            bottom: 80px;
            height: calc(100vh - 120px);
        }

        .floating-chat-bubble {
            bottom: 20px;
            right: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def _render_floating_chat():
    """Render the floating chat button."""

    # CSS to make the button container float in bottom-right
    st.markdown("""
    <style>
    /* Hide parent containers from page flow */
    .chat-button-wrapper {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        overflow: visible !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Float the button container to bottom-right */
    .chat-button-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 999999;
    }

    /* Style the Streamlit button */
    .chat-button-container button {
        height: 50px !important;
        border-radius: 25px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5) !important;
        border: none !important;
        padding: 12px 24px !important;
        animation: pulse-shadow 2s infinite !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        color: white !important;
        cursor: pointer !important;
    }

    .chat-button-container button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.7) !important;
    }

    .chat-button-container button p {
        margin: 0 !important;
        padding: 0 !important;
    }

    @keyframes pulse-shadow {
        0%, 100% { box-shadow: 0 4px 20px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 4px 30px rgba(102, 126, 234, 0.8); }
    }
    </style>
    """, unsafe_allow_html=True)

    # Render button wrapped in custom divs to hide from page flow
    st.markdown('<div class="chat-button-wrapper"><div class="chat-button-container">', unsafe_allow_html=True)
    if st.button("💬 Chat with HealthAI", key="chat_open_btn", type="primary"):
        st.session_state.chat_open = True
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


@st.dialog("💬 HealthAI Chat", width="large")
def _render_chat_dialog():
    """Render the chat dialog popup."""

    # Show context status
    if st.session_state.user_context and st.session_state.user_context.get('has_data'):
        st.caption("✅ Using your health data for personalized responses")
    else:
        st.caption("💡 Upload health data for personalized insights")

    # Chat content container
    with st.container():

        # Display chat history
        chat_container = st.container()
        with chat_container:
            history = st.session_state.chat_agent.get_conversation_history()

            if len(history) == 0:
                st.info("👋 Hi! I'm HealthAI. Ask me anything about your health data, biomarkers, or general health questions!")
            else:
                for message in history:
                    role = message.get("role", "user")
                    content = message.get("content", "")

                    if role == "user":
                        st.chat_message("user").write(content)
                    elif role == "assistant":
                        st.chat_message("assistant").write(content)

        # Chat input
        user_input = st.chat_input("Ask about your health...", key="chat_input")

        if user_input:
            # Display user message immediately
            with chat_container:
                st.chat_message("user").write(user_input)

            # Get AI response
            with st.spinner("HealthAI is thinking..."):
                response = st.session_state.chat_agent.chat(user_input)

            # Display assistant response
            with chat_container:
                st.chat_message("assistant").write(response)

            st.rerun()

        # Quick action buttons
        st.markdown("---")
        st.markdown("**Quick Actions:**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Explain My Results", key="quick_results", use_container_width=True):
                quick_prompt = "Can you explain my key biomarker results and what they mean for my health?"
                response = st.session_state.chat_agent.chat(quick_prompt)
                st.rerun()

        with col2:
            if st.button("💊 Supplement Advice", key="quick_supplements", use_container_width=True):
                quick_prompt = "What supplements do you recommend based on my analysis?"
                response = st.session_state.chat_agent.chat(quick_prompt)
                st.rerun()

        with col3:
            if st.button("🎯 Health Tips", key="quick_tips", use_container_width=True):
                quick_prompt = "What are the top 3 things I should focus on to improve my health?"
                response = st.session_state.chat_agent.chat(quick_prompt)
                st.rerun()

        # Additional options
        st.markdown("---")
        exp_col1, exp_col2 = st.columns(2)

        with exp_col1:
            if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
                st.session_state.chat_agent.reset_conversation()
                st.success("Chat cleared!")
                st.rerun()

        with exp_col2:
            if len(history) > 0:
                chat_export = st.session_state.chat_agent.export_chat_history()
                st.download_button(
                    label="📥 Export Chat",
                    data=chat_export,
                    file_name="healthai_chat_history.json",
                    mime="application/json",
                    use_container_width=True
                )

    # Close button in dialog
    if st.button("Close Chat", key="close_dialog_btn", type="secondary", use_container_width=True):
        st.session_state.chat_open = False
        st.rerun()
