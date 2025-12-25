from src.llm_chain.llm_builder import get_llm_model, get_llm_response
from src.llm_chain.prompt_template import clarification_required_hint
import json

def clarification_classifier(user_query):

    updated_query = clarification_required_hint.invoke({"user_query":user_query})
    
    model = get_llm_model()
    resp = get_llm_response(model, updated_query)

    json_body = json.loads(resp)
    final_decision = json_body["needs_clarification"]
    confidence_score = json_body["confidence"]
    reasoning = json_body["reasoning"]

    return {"decision" : final_decision, 
            "confidence_score" : confidence_score, 
            "reasoning" : reasoning}