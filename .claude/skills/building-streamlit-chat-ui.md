# Skill: Building Streamlit Chat UI

<!--
Purpose: Chat interface patterns — messages, streaming, file uploads, audio, feedback.
Source: https://github.com/the-ai-buildr/st-agent-skills (building-streamlit-chat-ui)
-->

## When to Use

Creating conversational UIs, chatbots, or AI assistants in Streamlit.

## Key Patterns

- `st.chat_message(role)` + `st.chat_input()` as the basic structure.
- Persist messages in `st.session_state.messages` as a list of `{"role": ..., "content": ...}` dicts.
- `st.write_stream(generator)` for streaming token-by-token; can pass an OpenAI stream object directly.
- Custom avatars: `:material/robot:` icons or image URLs in `st.chat_message`.
- Suggestion chips: `st.pills()` shown only when `not st.session_state.messages`.
- File uploads: `accept_file=True` on `st.chat_input`; returns object with `.text` and `.files`.
- Audio input: `accept_audio=True`; use speech-to-text and inject transcript via session state + `st.rerun()`.
- Feedback: `st.feedback("thumbs")` — also supports `"stars"`, `"faces"`.
- Clear chat: callback that resets `st.session_state.messages = []`.

## Pattern

```python
import streamlit as st

st.session_state.setdefault("messages", [])

# Suggestion chips (only when chat is empty)
if not st.session_state.messages:
    prompt_hint = st.pills(
        "Try asking",
        ["What is the kill mud weight?", "Show annular velocity formula"],
        label_visibility="collapsed",
    )
    if prompt_hint:
        st.session_state.messages.append({"role": "user", "content": prompt_hint})
        st.rerun()

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if user_input := st.chat_input("Ask a drilling question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant", avatar=":material/robot:"):
        response = st.write_stream(get_ai_response(user_input))
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear button
if st.button(":material/delete: Clear chat"):
    st.session_state.messages = []
    st.rerun()
```
