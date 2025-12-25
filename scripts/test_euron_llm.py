#For script run
import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.llm_chain.prompt_template import retrieval_use_hint

api_key = os.getenv("EURON_KEY")


from euriai.langchain import create_chat_model

chat_model = create_chat_model(
    api_key=api_key,
    model="gpt-4.1-nano",
    temperature=0.7
)

_query= "name 1 animal"

response = chat_model.invoke(_query)
print(response.content)
