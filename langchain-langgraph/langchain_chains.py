#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#---------------------------------------------------------------------------

from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.llm_chain.llm_builder import get_llm_model

joke_topic = input("enter your joke topic: ")

string_output = StrOutputParser()

my_prompt = PromptTemplate(input_variables=["topic"],  
                           template= "generate a short joke on the topic {topic}")

llm_model = get_llm_model(temp=0.9)

#runnable sequence = LCEL
#runnable_seq = RunnableSequence(my_prompt, llm_model, string_output)

runnable_seq = my_prompt | llm_model | string_output

print(runnable_seq.invoke({"topic":joke_topic}))

