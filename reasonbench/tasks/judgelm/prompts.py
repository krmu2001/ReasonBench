system = "You are a helpful and precise assistant for checking the quality of the answer."

judge_single = (
"We would like to request your feedback on the performance of two AI assistants "
"in response to the user question displayed above.\n"
"Please rate the helpfulness, relevance, accuracy, level of details of their "
"responses. Each assistant receives an overall score on a scale of 1 to 10, "
"where a higher score indicates better overall performance.\n"
"Please first output a single line containing only two values indicating the "
"scores for Assistant 1 and 2, respectively. The two scores are separated by a "
"space. In the subsequent line, please provide a comprehensive explanation of "
"your evaluation, avoiding any potential bias and ensuring that the order in "
"which the responses were presented does not affect your judgment."
)

judge_single_template = (
    "[Question]\n{question}\n\n"
    "[The Start of Assistant 1's Answer]\n{answer_1}\n\n"
    "[The End of Assistant 1's Answer]\n\n"
    "[The Start of Assistant 2's Answer]\n{answer_2}\n\n"
    "[The End of Assistant 2's Answer]\n\n"
    "[System]\n{prompt}\n\n"
)