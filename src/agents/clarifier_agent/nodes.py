"""https://chatgpt.com/share/695171c4-9920-800b-b22a-f2b68c9b8e54"""


from state.state_schema import StateSchema
from prompt_templates.prompt_clarifier_agent import ambiguity_check_prompt, clarification_question_generation_prompt, user_query_consolidation_prompt


"""nodes of the graph"""

AMBIGUITY_CHECKER = "ambiguity_checker"
CLASSIFIER_QUES_GEN = "classfier_ques_generator"
CONSOLIDATOR = "intent_consolidator"
WAIT_FOR_USER = "wait_for_user"
CHECK_FOR_STOP = "check_for_stop"

def ambiguity_checker(state: StateSchema):
    pass

