
from langchain.agents import create_pandas_dataframe_agent,Tool,initialize_agent,AgentType
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
import pandas as pd
import matplotlib.pyplot as plt
from langchain.chat_models import ChatOpenAI
import streamlit as st
import time
import os 
os.environ["OPENAI_API_KEY"]="sk-IxW"+"GL6i3pIk3j8LsSX"+"38T3BlbkFJJ63Iv84bpgC"+"n2CrtrFbH"
import langchain
langchain.debug=False
st.markdown("<h1 align=center>LightHouse Chat Demo</h1>",unsafe_allow_html=True)
def house():
    llm=OpenAI(model="text-davinci-003",temperature=0.7)
    # llm=ChatOpenAI(model="gpt-4",temperature=0)
    df=pd.read_excel("lighthouse6_u.xlsx")
    df_agent=create_pandas_dataframe_agent(llm,df,verbose=True)
    tools=[
        Tool(
            name="Lighthouses",
            func=df_agent.run,
            description="""useful for when you need to answer questions about Lighthouses and relevent details.
            - \nyou should use streamlit pyplot function to give visulization
            - \nWhen user ask about graphs like visualization then you should use python_repl_ast Action to print the Graph using st.pyplot beacuase here we print this streamlit . 
            - \nWhen 2 are responses found then take first one and also When User ask about today then show first row date results for Example: take recent date from dataframe
            - \ntoday Date : first row date of dataset , don't take current date
            - \nWhen User ask about Status you should the lighthouse is on or off
            - \nAfter Finishing Time you should print AI:Observation directly:
                Ex: Observation: 6 lighthouses are available.
                   Thought: Do I need to use a tool? No
                   AI: 6 lighthouses are available
            - \nGive the Direct Final Answer it may have any length just give direct final answer
                        The Lighthouses are :
                        BishopRock 
                        Flotta_Grinds_Buoy
                        Dunnet_Head          
                        BullPointPost
                        Balta_Sound
                        Eddystone
            - \nWhen user ask about lighthouse you should give response from lighthouse tool,don't give based on your knowledge
            - \nAttension Don't include North Point, South Point, East Point, West Point, Central Point, and Far Point in any responses.this are not lighthouses availble in given data.if you give this again i'm not satisfied with your response.so please don't include.
            - \nThe lighthouses that are Off are North Point, South Point, East Point, West Point, Central Point, and Far Point.
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
                message_placeholder.write(full_response + "▌")
            message_placeholder.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
house()
