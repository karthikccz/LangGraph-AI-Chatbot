import streamlit as st
from backend.backend import chatbot,retrieve_all_threads
from backend.database import get_all_chat_titles,save_chat_title,delete_chat
from langchain_core.messages import HumanMessage
import uuid


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_thread_id():
    """
    Generate a unique thread ID for every new conversation.
    """
    return str(uuid.uuid4())


def add_thread(thread_id):
    """
    Add thread to the Streamlit conversation list.
    """

    thread_id = str(thread_id)

    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def get_chat_name(thread_id):
    """
    Get the custom chat name.
    If no name exists, return a default name.
    """

    thread_id = str(thread_id)

    return st.session_state["chat_names"].get(
        thread_id,
        f"Chat {thread_id[:8]}"
    )


def reset_chat():
    """
    Create and open a new chat.
    """

    new_thread_id = generate_thread_id()

    # Set new thread as active thread
    st.session_state["thread_id"] = new_thread_id

    # Add to conversation list
    add_thread(new_thread_id)

    # Give default name
    st.session_state["chat_names"][new_thread_id] = "New Chat"

    # Clear displayed messages
    st.session_state["message_history"] = []

    st.rerun()


def load_conversation(thread_id):
    """
    Load conversation messages from LangGraph SQLite checkpointer.
    """

    thread_id = str(thread_id)

    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


def select_chat(thread_id):
    """
    Select and load an existing chat.
    """

    thread_id = str(thread_id)

    # Set selected thread as active
    st.session_state["thread_id"] = thread_id

    # Load messages from database
    messages = load_conversation(thread_id)

    temp_messages = []

    for msg in messages:

        # Identify user message
        if isinstance(msg, HumanMessage):
            role = "user"

        # Otherwise assume AI message
        else:
            role = "assistant"

        temp_messages.append(
            {
                "role": role,
                "content": msg.content
            }
        )

    # Update Streamlit message history
    st.session_state["message_history"] = temp_messages


def rename_chat(thread_id, new_name):
    """
    Rename a chat permanently.
    """

    thread_id = str(thread_id)

    if new_name.strip():

        new_name = new_name.strip()

        # Save name permanently in SQLite database
        save_chat_title(thread_id, new_name)

        # Update Streamlit session
        st.session_state["chat_names"][thread_id] = new_name


def delete_chat_ui(thread_id):
    """
    Permanently delete a conversation.
    """

    thread_id = str(thread_id)

    # Delete conversation from database
    delete_chat(thread_id)

    # Remove from Streamlit chat list
    if thread_id in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].remove(thread_id)

    # Remove title from session state
    if thread_id in st.session_state["chat_names"]:
        del st.session_state["chat_names"][thread_id]

    # If currently active chat is deleted
    if str(st.session_state["thread_id"]) == thread_id:

        # Create a new chat
        new_thread_id = generate_thread_id()

        st.session_state["thread_id"] = new_thread_id

        add_thread(new_thread_id)

        # Default name
        st.session_state["chat_names"][new_thread_id] = "New Chat"

        # Clear UI
        st.session_state["message_history"] = []

    st.rerun()


# ============================================================
# SESSION STATE SETUP
# ============================================================

# Message history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


# Current active thread
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


# Load all existing conversations
if "chat_threads" not in st.session_state:

    database_threads = retrieve_all_threads()

    # Convert all thread IDs to strings
    st.session_state["chat_threads"] = [
        str(thread_id)
        for thread_id in database_threads
    ]


# Load saved chat names
if "chat_names" not in st.session_state:

    st.session_state["chat_names"] = get_all_chat_titles()


# Add current thread to list
add_thread(st.session_state["thread_id"])


# Add default names for chats without names
for thread_id in st.session_state["chat_threads"]:

    thread_id = str(thread_id)

    if thread_id not in st.session_state["chat_names"]:

        st.session_state["chat_names"][thread_id] = (
            f"Chat {thread_id[:8]}"
        )


# ============================================================
# SIDEBAR UI
# ============================================================

st.sidebar.title("🤖 LangGraph Chatbot")


# ------------------------------------------------------------
# NEW CHAT BUTTON
# ------------------------------------------------------------

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):
    reset_chat()


st.sidebar.divider()

st.sidebar.header("💬 My Conversations")


# ------------------------------------------------------------
# DISPLAY ALL CONVERSATIONS
# ------------------------------------------------------------

for thread_id in st.session_state["chat_threads"][::-1]:

    thread_id = str(thread_id)

    chat_name = get_chat_name(thread_id)

    # Three columns:
    # Chat Name | Rename | Delete
    col1, col2, col3 = st.sidebar.columns(
        [6, 1, 1]
    )


    # --------------------------------------------------------
    # SELECT CHAT
    # --------------------------------------------------------

    with col1:

        if st.button(
            chat_name,
            key=f"select_{thread_id}",
            use_container_width=True
        ):

            select_chat(thread_id)

            st.rerun()


    # --------------------------------------------------------
    # RENAME CHAT
    # --------------------------------------------------------

    with col2:

        if st.button(
            "✏️",
            key=f"rename_{thread_id}",
            help="Rename chat"
        ):

            st.session_state["editing_thread"] = thread_id

            # Remove delete mode if active
            if "deleting_thread" in st.session_state:
                del st.session_state["deleting_thread"]

            st.rerun()


    # --------------------------------------------------------
    # DELETE CHAT
    # --------------------------------------------------------

    with col3:

        if st.button(
            "🗑️",
            key=f"delete_{thread_id}",
            help="Delete chat"
        ):

            st.session_state["deleting_thread"] = thread_id

            # Remove rename mode if active
            if "editing_thread" in st.session_state:
                del st.session_state["editing_thread"]

            st.rerun()


# ============================================================
# RENAME CHAT SECTION
# ============================================================

if "editing_thread" in st.session_state:

    editing_thread = st.session_state["editing_thread"]

    st.sidebar.divider()

    st.sidebar.subheader("✏️ Rename Chat")


    new_name = st.sidebar.text_input(
        "Enter new chat name",
        value=get_chat_name(editing_thread),
        key=f"rename_input_{editing_thread}"
    )


    col1, col2 = st.sidebar.columns(2)


    # SAVE BUTTON
    with col1:

        if st.button(
            "Save",
            key=f"save_rename_{editing_thread}",
            use_container_width=True
        ):

            rename_chat(
                editing_thread,
                new_name
            )

            del st.session_state["editing_thread"]

            st.rerun()


    # CANCEL BUTTON
    with col2:

        if st.button(
            "Cancel",
            key=f"cancel_rename_{editing_thread}",
            use_container_width=True
        ):

            del st.session_state["editing_thread"]

            st.rerun()


# ============================================================
# DELETE CONFIRMATION SECTION
# ============================================================

if "deleting_thread" in st.session_state:

    deleting_thread = st.session_state["deleting_thread"]

    st.sidebar.divider()

    st.sidebar.warning(
        f"Delete '{get_chat_name(deleting_thread)}'?"
    )


    col1, col2 = st.sidebar.columns(2)


    # --------------------------------------------------------
    # CONFIRM DELETE
    # --------------------------------------------------------

    with col1:

        if st.button(
            "Yes, Delete",
            key=f"confirm_delete_{deleting_thread}",
            use_container_width=True
        ):

            # Remove state before deleting
            del st.session_state["deleting_thread"]

            delete_chat_ui(deleting_thread)


    # --------------------------------------------------------
    # CANCEL DELETE
    # --------------------------------------------------------

    with col2:

        if st.button(
            "Cancel",
            key=f"cancel_delete_{deleting_thread}",
            use_container_width=True
        ):

            del st.session_state["deleting_thread"]

            st.rerun()


# ============================================================
# MAIN CHAT UI
# ============================================================

st.title(
    f"💬 {get_chat_name(st.session_state['thread_id'])}"
)


# ------------------------------------------------------------
# DISPLAY MESSAGE HISTORY
# ------------------------------------------------------------

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Type your message here..."
)


if user_input:

    # --------------------------------------------------------
    # ADD USER MESSAGE TO UI HISTORY
    # --------------------------------------------------------

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)


    # --------------------------------------------------------
    # LANGGRAPH CONFIGURATION
    # --------------------------------------------------------

    CONFIG = {

        "configurable": {

            "thread_id": str(
                st.session_state["thread_id"]
            )
        },

        "metadata": {

            "thread_id": str(
                st.session_state["thread_id"]
            )
        },

        "run_name": "chat_turn",
    }


    # --------------------------------------------------------
    # GET STREAMING AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        ai_message = st.write_stream(

            message_chunk.content

            for message_chunk, metadata
            in chatbot.stream(

                {
                    "messages": [
                        HumanMessage(
                            content=user_input
                        )
                    ]
                },

                config=CONFIG,

                stream_mode="messages"

            )

            # Avoid empty chunks
            if message_chunk.content
        )


    # --------------------------------------------------------
    # SAVE AI RESPONSE TO UI HISTORY
    # --------------------------------------------------------

    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )