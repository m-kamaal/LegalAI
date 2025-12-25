from euriai.langchain import create_chat_model
from dotenv import load_dotenv
import os
load_dotenv()
_euron_llm_key = os.getenv("EURON_KEY")

def get_llm_model(llm_key =_euron_llm_key, model_id="gpt-4.1-nano", temp = 0.6):
     model = create_chat_model(api_key= llm_key, model=model_id, temperature= temp)
     return model

def get_llm_response(model_object, query):
     resp = model_object.invoke(query)
     return resp.content



if __name__ == "__main__":

     pass