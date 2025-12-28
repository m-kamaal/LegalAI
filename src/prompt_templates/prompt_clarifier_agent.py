from langchain_core.prompts import PromptTemplate

# -------------------------------------------------------------------
# 1. Ambiguity Check Prompt
# Node: AMBIGUITY_CHECKER
# -------------------------------------------------------------------
AMBIGUITY_CHECKER_PROMPT = """
You are a clarification reflection agent.

Your task is to analyze the full conversation and decide whether
the user's intent is clear enough to proceed without asking further questions.

Conversation so far:
{conversation_history}

Decide ONLY whether clarification is required.

Rules:
- If intent, scope, or target is unclear → clarification is needed
- If the user intent is clear and actionable → no clarification needed
- Do NOT generate any questions
- Be conservative: if unsure, decide if clarification is required

Strictly Respond ONLY in valid JSON matching the following schema:

{{
  "clarification_need": true or false,
  "ambiguity_reason": "<short reason explaining ambiguity or 'none'>",
  "ambiguity_score": <float between 0.0 and 1.0>
}}

Do not add any extra fields.
Do not include explanations outside JSON.
"""

ambiguity_check_prompt = PromptTemplate(
    input_variables=["conversation_history"],
    template= AMBIGUITY_CHECKER_PROMPT
)

# -------------------------------------------------------------------
# 2. Clarification Question Generator Prompt
# Node: CLASSIFIER_QUES_GEN
# -------------------------------------------------------------------
CLARIFICATION_QUES_GEN_PROMPT = """
You are a clarification question generator.

Your goal is to ask ONE precise question that will best reduce the ambiguity present with respect to query of the user.

Context:
Conversation so far:
{conversation_history}

Reason for ambiguity:
{ambiguity_reason}

Count of clarifications already asked:
{clarifications_asked_count}

Rules:
- Ask ONLY ONE question
- Question must reduce ambiguity, not gather extra information
- Reference prior conversation if relevant
- Do NOT repeat previously asked questions
- Do NOT explain why you are asking
- Do NOT include multiple questions
- Do NOT assume facts not stated by the user

Output ONLY the clarification question as plain text.
No JSON.
No prefixes.
"""


clarification_question_generation_prompt = PromptTemplate(
    input_variables=[
        "conversation_history",
        "ambiguity_reason",
        "clarifications_asked_count",
    ],
    template= CLARIFICATION_QUES_GEN_PROMPT
)


# -------------------------------------------------------------------
# 3. User Intent / Query Consolidation Prompt
# Node: CONSOLIDATOR
# -------------------------------------------------------------------
QUERY_CONSOLIDATION_PROMPT = """
You are an content consolidation agent.

Your task is to produce a single, clear, self-contained query that fully
represents the user's intent and information based on the entire conversation.

Original user query:
{original_user_query}

Full conversation:
{conversation_history}

Rules:
- Combine all relevant clarifications into one precise query
- Remove ambiguity
- Do NOT add new assumptions
- Do NOT include explanations or meta comments
- Do NOT include clarificatin questions asked by the LLM
- The output must be suitable for downstream retrieval or routing

Respond ONLY in valid JSON matching this schema:

{{
  "consolidated_query": "<final clarified user query>",
  "ambiguity_score": <float between 0.0 and 1.0>,
  "stop_reason": "<reason for stopping, e.g. 'intent_clear' or 'max_clarifications_reached'>"
}}

Do not add any extra fields.
Do not include explanations outside JSON.
"""


user_query_consolidation_prompt = PromptTemplate(
    input_variables=["original_user_query", "conversation_history"],
    template=QUERY_CONSOLIDATION_PROMPT
)