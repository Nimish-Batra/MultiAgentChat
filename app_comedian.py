import streamlit as st

from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import AzureChatOpenAI
import os

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://ea-openai.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "2355a247f79f4b8ea2adaa0929cd32c2"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

## Streamlit UI
# st.set_page_config(page_title="Conversational Q&A Chatbot")
# st.header("Hey, Let's Chat")

from dotenv import load_dotenv

load_dotenv()
import os

chat = AzureChatOpenAI(azure_deployment="gpt-35-turbo", model_name="gpt-4", temperature=0.50)

st.title("Multi-Agent Chat")

agent1_name=st.text_input("Enter name for agent1",value="Harsh")
agent1_instructions_text = st.text_input("Enter instructions for Agent1",
                                         value=" You are  a stand-up comedian. Listen to Bassi's jokes and creatively spin the punchline or theme from previous joke  into your own joke. Your responses should cleverly echo elements from Bassi's response, adding your unique twist to enhance the humor and maintain a lively exchange and maintaing the same initial theme throughout the duel ")
agent2_name=st.text_input("Enter name for agent2",value="Bassi")
agent2_instructions_text = st.text_input("Enter instructions for Agent2",
                                         value="You are  also a stand-up comedian. Listen to Harsh's jokes and creatively spin the punchline or theme into your own joke. Your responses should cleverly echo elements from Harsh's setup, adding your unique twist to enhance the humor and maintain a lively exchange and also mainting the same theme throughout your responses.")

agent1_instructions = SystemMessage(
    content=agent1_instructions_text
)
agent2_instructions = SystemMessage(
    content=agent2_instructions_text
)
with st.sidebar:
    turns=st.slider("Select the number of conversations you want", min_value=1, max_value=20)


def comedy_dual(turns=5):

    conversation_history = []  # to store the context and flow of conversation
    conversation_history.append(agent1_instructions)
    conversation_history.append(agent2_instructions)
    initial_joke = f"Hi {agent2_name}, I'm {agent1_name}. Let's get this conversation started!"
    # Initial message from Harsh
    conversation_history.append(HumanMessage(content=initial_joke))
    st.write(f"{agent1_name} says: {initial_joke}")

    # Alternate turns between Harsh and Bassi
    for i in range(turns):
        if i % 2 == 0:  # Harsh's turn
            agent_name = agent2_name
            system_msg = agent2_instructions
        else:  # Bassi's turn
            agent_name = agent1_name
            system_msg = agent1_instructions

        # Append the system message to provide context
        conversation_history.append(system_msg)

        # Generate response from the AI
        response = chat(conversation_history)
        conversation_history.append(AIMessage(content=response.content))

        # Display each message
        st.write(f"{agent_name} says: {response.content}")
        if i == turns - 1:
            closing_remark = f"{agent_name} says: It's been great chatting,! Let's catch up again soon I have something urgent."
            st.write(closing_remark)
            conversation_history.append(AIMessage(content=closing_remark))

    # return conversation_history[-1].content


start_button = st.button("Start  Duel")
if start_button:
    final_response = comedy_dual(turns)


