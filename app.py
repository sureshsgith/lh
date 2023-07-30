
from langchain.agents import create_pandas_dataframe_agent,Tool,initialize_agent,AgentType
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
import pandas as pd
from langchain.chat_models import ChatOpenAI
import streamlit as st
import time
import os 
os.environ["OPENAI_API_KEY"]="sk-IxW"+"GL6i3pIk3j8LsSX"+"38T3BlbkFJJ63Iv84bpgC"+"n2CrtrFbH"
import langchain
langchain.debug=False
st.markdown("<h1 align=center>LightHouse Chat Demo</h1>",unsafe_allow_html=True)
def house():
    llm=OpenAI(model="text-davinci-003",temperature=0)
    # llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0)
    df=pd.read_csv("lighthouse_5.csv")
    df_agent=create_pandas_dataframe_agent(llm,df,verbose=True)

    tools=[
        Tool(
            name="Lighthouses",
            func=df_agent.run,
            description="""useful for when you need to answer questions about Light houses.
            - if prompt contains table then you should replace with Table format then you should use pandas style format function
            - Whenever you ask for visualizations such as graphs, tables, or line charts, you need to provide the responses in a resepected format.for example
            - If the Query is related to visualization then you need consider visualization at in prompt.and give the direct answer
            
            - You should give the table at below 
             
            - The date should be taken as dd-mm-yyyy( ex: 01-02-2023).
            - Note: Don't Give Response According to you.give only according to data. 
            - When 2 are responses found then take first one and also When User ask about today then show first row date results for Example:the first row have date 30-06-2023 then give the results of 30-06-2023 date, Don't take your own date.
            - today Date : first row date of dataset , don't take current date
            - When User ask about Status you should the lighthouse is on or off
            - After Finishing Time you should print AI:Observation directly:
                Ex: Observation: 16 lighthouses are available.
                   Thought: Do I need to use a tool? No
                   AI: 16 lighthouses are available
            - Give the Direct Final Answer it may have any length just give direct final answer
             For example :
             
Observation: Trevose               1188
WolfRock              1066
Lizard                1065
BishopRock            1050
Sumburgh_Head          982
Godrevy                912
North_Rona             818
Sule_Skerry            816
Flotta_Grinds_Buoy     816
North_Ronaldsay        812
Dunnet_Head            810
BullPointPost          768
Balta_Sound            660
Eddystone              653
BullPointPre            58
Thought: I now know the final answer
Final Answer: There are 16 lighthouses and the table shows how many times each lighthouse has been turned. ( it shoud not be)
            Final Answer Not to be : There are 16 lighthouses and the table shows how many times each lighthouse has been turned.
            Final Answer Should be : Trevose               1188
WolfRock              1066
Lizard                1065
.                       
.
.
Eddystone              653
BullPointPre            58

                

            Lets think step by step."""
        ),
    ]
    def get_memory():
        if "memory" not in st.session_state:
            st.session_state.memory = ConversationBufferMemory(memory_key="chat_history")
        return st.session_state.memory

    memory = get_memory()
    agent_chain=initialize_agent(tools,llm,agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,verbose=True,memory=memory)



    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            ai_response=agent_chain.run(prompt)
            for chunk in ai_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
house()
