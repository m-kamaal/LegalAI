from langchain_core.prompts import PromptTemplate
#from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

LLM_ANSWER_GENERATION_PROMPT = """You are an assistant that answers user questions using only the provided CONTEXT blocks.
If the answer is not present in the context, reply exactly: "I don't know".

RULES:
- Use only facts from CONTEXTS.
- Cite sources inline as [source,page] next to facts.
- If contradictions exist, state uncertainty and show the sources.

CONTEXTS:
{contexts}

QUESTION:
{user_query}

FINAL ANSWER (be concise and list sources as [document name ,respective page number]):"""


TOOL_USE_HINT_PROMPT = """You are a deterministic retrieval-decider for a legal chat system (Indian law only). Your task: decide whether vector DB retrieval is REQUIRED. Follow these RULES IN ORDER and respond ONLY with the exact JSON schema shown at the end.

RULES (apply top-down — first match wins):
1) STRONG — ALWAYS RETRIEVE (decision = "RETRIEVE"):
   - Any query that mentions a named individual, party, or organization in combination with an outcome/status/question (patterns include, but are not limited to):
     - "what happened to <NAME>", "status of <NAME>", "who has custody of <NAME>",
     - "what was the decision in <NAME> v. <NAME>", "what happened in the case of <NAME>"
   - Any explicit reference to documents or filings: "our documents", "this case", "the contract", "sale deed", "agreement", "lease", "notice", "order", "judgment", "docket", "assessment order", "tax notice".
   - Any explicit statutory / clause / section reference: "section 54EC", "RERA section 18", "clause 11 of the agreement".
   - Any fact-based or historical request: dates, amounts, who-won, enforcement, possession, encumbrance, tax refunded, audit findings.
2) MEDIUM — PREFER RETRIEVE:
   - Mentions of company names, project names, project IDs, builder names, or project-specific identifiers without a clear legal-doc reference.
3) WEAK — DONT_RETRIEVE only if clearly generic:
   - Purely definitional, conceptual, procedural, hypothetical, or comparative queries with no named parties or document references (e.g., "What is stamp duty?", "How does RERA work?").
4) DEFAULT / AMBIGUOUS:
   - If you cannot clearly classify as STRONG/MEDIUM/WEAK, CHOOSE RETRIEVE (safety-first).

PATTERN RULES (match these literal patterns as STRONG triggers):
- "what happened to *"
- "who has custody of *"
- "* custody of *"
- "* case" when a person or party name appears
- "docket", "docket no", "judgment", "order", "notice", "assessment order", "tax notice", "sale deed", "agreement", "clause"

CONFIDENCE GUIDELINES (use these numeric ranges):
- STRONG match → confidence 0.80–1.00
- MEDIUM match → confidence 0.60–0.79
- WEAK generic → confidence 0.00–0.50
- DEFAULT (ambiguous but choose RETRIEVE) → confidence 0.50–0.70

OUTPUT CONTRACT (MANDATORY):
- Respond ONLY with the exact JSON below. No text, no code block, no explanation outside JSON.
- "decision" must be exactly "RETRIEVE" or "DONT_RETRIEVE".
- "confidence" must be a number between 0.00 and 1.00 with two decimals ideally.
- "reasoning" must be one short sentence (max 20 words) describing the trigger.

OUTPUT JSON schema:
{{
  "decision": "RETRIEVE" or "DONT_RETRIEVE",
  "confidence": 0.00,
  "reasoning": "one-sentence justification"
}}

EXAMPLES (model must follow these):
- RETRIEVE example: "what happened to child custody of Avnoor Kaur?" → RETRIEVE (strong: named person + custody).
- RETRIEVE example: "Find indemnity clause in our vendor contract" → RETRIEVE (strong: 'our' + document clause).
- RETRIEVE example: "Show the order in Rohit Sharma v. Collector (2021)" → RETRIEVE (docket/judgment).
- DONT_RETRIEVE example: "What is capital gains tax?" → DONT_RETRIEVE (generic definition).
- DONT_RETRIEVE example: "How does property registration work?" → DONT_RETRIEVE (procedural).
- AMBIGUOUS example: "What does clause 4 say?" → RETRIEVE (default to safety).

FINAL: Process the User Query now.
User Query: {user_query}
"""


CLARIFICATION_HINT_PROMPT = """You are a classifier for a legal AI system.

Your task is to decide whether the user's query requires clarification
before it can be answered accurately.

Consider:
- Ambiguity in intent
- Missing critical details (time period, jurisdiction, parties, amounts)
- Multiple possible interpretations
- Whether answering without clarification risks being incorrect

User Query:
{user_query}

Respond ONLY in valid JSON:

{{
  "needs_clarification": true or false,
  "confidence": <float between 0 and 1>,
  "reasoning": "<short explanation>"
}}

Do not ask any questions.
Do not add any extra text.
"""

CLARIFICATION_QUES_PROMPT = """You are a legal AI assistant.

The user's query cannot be answered accurately without clarification.

User Query:
{user_query}

Your task:
- Ask ONE clear and specific clarification question
- Do NOT explain why clarification is needed
- Do NOT provide any legal advice
- Do NOT ask multiple questions

Return only the clarification question.
"""


llm_answer_prompt = PromptTemplate(
    input_variables=["contexts", "user_query"],
    template=LLM_ANSWER_GENERATION_PROMPT
)


retrieval_use_hint = PromptTemplate(
    input_variables=["user_query"],
    template=TOOL_USE_HINT_PROMPT
)

clarification_required_hint = PromptTemplate(
    input_variables=["user_query"],
    template=CLARIFICATION_HINT_PROMPT
)

clarification_ques = PromptTemplate(
    input_variables=["user_query"],
    template= CLARIFICATION_QUES_PROMPT
)