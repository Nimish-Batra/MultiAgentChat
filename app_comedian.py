import streamlit as st

from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain.chat_models import AzureChatOpenAI
import os

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://ea-openai.openai.azure.com/"
main_key=os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

## Streamlit UI
# st.set_page_config(page_title="Conversational Q&A Chatbot")
# st.header("Hey, Let's Chat")

from dotenv import load_dotenv
load_dotenv()
import os

chat=AzureChatOpenAI(azure_deployment="gpt-35-turbo", model_name="gpt-4", temperature=0.50)

st.title("Multi-Agent Chat")

harsh_instructions_text = st.text_input("Enter instructions for Harsh", value=" You are Harsh, a stand-up comedian. Listen to Bassi's jokes and creatively spin the punchline or theme from previous joke  into your own joke. Your responses should cleverly echo elements from Bassi's response, adding your unique twist to enhance the humor and maintain a lively exchange and maintaing the same initial theme throughout the duel ")
bassi_instructions_text = st.text_input("Enter instructions for Bassi", value="You are Bassi, also a stand-up comedian. Listen to Harsh's jokes and creatively spin the punchline or theme into your own joke. Your responses should cleverly echo elements from Harsh's setup, adding your unique twist to enhance the humor and maintain a lively exchange and also mainting the same theme throughout your responses.")

harsh_instructions = SystemMessage(
    content=harsh_instructions_text
)
bassi_instructions = SystemMessage(
    content=bassi_instructions_text
)

def comedy_dual(turns=5):
    conversation_history = []  # to store the context and flow of conversation
    initial_joke="Hey I am Harsh. Bassi ,Let's keep the conversation rolling"
    # Initial message from Harsh
    conversation_history.append(HumanMessage(content=initial_joke))
    st.write(f"Harsh says: {initial_joke}")

    # Alternate turns between Harsh and Bassi
    for i in range(turns):
        if i % 2 == 0:  # Harsh's turn
            agent_name = "Bassi"
            system_msg = bassi_instructions
        else:  # Bassi's turn
            agent_name = "Harsh"
            system_msg =harsh_instructions

        # Append the system message to provide context
        conversation_history.append(system_msg)

        # Generate response from the AI
        response = chat(conversation_history)
        conversation_history.append(AIMessage(content=response.content))

        # Display each message
        st.write(f"{agent_name} says: {response.content}")

    return conversation_history[-1].content

start_button = st.button("Start  Duel")
if start_button:
    final_response = comedy_dual()
