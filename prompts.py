from langchain.prompts import PromptTemplate

# Define prompt templates
prompt_templates = {
    "Short Summary": PromptTemplate(
        template="Summarize the following text in a {level} and informative manner: {text}",
        input_variables=["level", "text"]
    ),
    "Bullet Points": PromptTemplate(
        template="Summarize the following text using {level} bullet points: {text}",
        input_variables=["level", "text"]
    ),
    "Concise Paragraph": PromptTemplate(
        template="Summarize the following text in a {level} concise paragraph: {text}",
        input_variables=["level", "text"]
    ),
    "Key Takeaways": PromptTemplate(
        template="Extract the key takeaways from the following text at a {level} level: {text}",
        input_variables=["level", "text"]
    ),
    "Contextual Summary": PromptTemplate(
        template="Summarize the following text from the perspective of {audience} at a {level} level: {text}",
        input_variables=["audience", "level", "text"]
    ),
    "Evaluate Text": PromptTemplate(
        template="""Evaluate the following text based on the following criteria:
        1. **Clarity**: How clear and easy to understand is the text? (1-5)
        2. **Conciseness**: Does the text get to the point without unnecessary elaboration? (1-5)
        3. **Coherence**: Does the text flow logically, with smooth transitions between ideas? (1-5)
        4. **Grammar**: Are there any grammatical or syntactical errors? (1-5)
        5. **Tone**: Is the tone of the text appropriate for the target audience? (1-5)
        6. **Impact**: Does the text engage or persuade effectively? (1-5)
        7. **Readability**: How accessible is the text to a general audience? (1-5)
        Provide an overall score and specific suggestions for improvement.
        Text: {text}""",
        input_variables=["text"]
    ),
    "Paraphrase Text": PromptTemplate(
        template="Paraphrase the following text in a different way: {text}",
        input_variables=["text"]
    ),
    "Expand Text": PromptTemplate(
        template="Expand the following text with more details and explanation: {text}",
        input_variables=["text"]
    )
}
