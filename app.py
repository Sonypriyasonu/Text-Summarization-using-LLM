import streamlit as st
from summarization import TextSummarizer
from prompts import prompt_templates  

summarizer = TextSummarizer()

def main():
    st.title("Text Summarization & Evaluation")

    summary_type = st.selectbox("Select Summary Type", [
        "Short Summary",
        "Bullet Points",
        "Concise Paragraph",
        "Key Takeaways",
        "Contextual Summary",
        "Evaluate Text",
        "Paraphrase Text",
        "Expand Text"
    ])

    # Get the detail level for summaries
    if summary_type in ["Short Summary", "Bullet Points", "Concise Paragraph", "Key Takeaways", "Contextual Summary"]:
        detail_level = st.selectbox("Select Detail Level", ["Very Brief", "Moderately Brief", "Slightly Detailed"], index=1)
    else:
        detail_level = None

    # Get the audience for contextual summaries
    if summary_type == "Contextual Summary":
        audience = st.selectbox("Select Audience", ["Students", "Professionals", "General Public"], index=2)
    else:
        audience = None

    # Get the text input from the user
    text_input = st.text_area("Enter the text to be summarized/evaluated:")
    
    if text_input:
        word_count = len(text_input.split())

        # Check for profanity
        if summarizer.contains_profanity(text_input):
            st.error("Warning: Abusive or offensive language detected. Please modify your input.")

        # Check for confidential information
        if summarizer.contains_confidential_info(text_input):
            st.warning("Potentially sensitive or confidential information detected (e.g., email, phone number, SSN).")
            
            # Ask the user if they want to proceed despite the confidential info
            proceed = st.radio("Do you wish to proceed despite the sensitive information?", ["Yes", "No"])

            if proceed == "No":
                st.stop()  # Stop further processing if user decides not to proceed
                
        else:
            # Display word count if no issues detected
            st.write(f"**Word Count**: {word_count}")
        
    # Submit button
    if text_input and st.button("Submit"):
        # Choose the correct prompt template based on the summary type
        prompt_template = prompt_templates[summary_type]
        
        if summary_type == "Evaluate Text":
            # Ensure tracing is enabled here for LangChainTracer
            
            summary, prompt_tokens, response_tokens, total_tokens = summarizer.generate_summary(text_input, prompt_template)
            
            # Display the evaluation result
            if summary:
                st.write(f"**Word Count**: {word_count}")
                st.write(f"**Length**: {len(text_input)} characters")
                st.write("**Evaluation**:")
                st.write(summary)
                st.write(f"**Prompt tokens**: {prompt_tokens}")
                st.write(f"**Response tokens**: {response_tokens}")
                st.write(f"**Total tokens used**: {total_tokens}")
            else:
                st.error("Evaluation failed.")
        
        else:           
            summary, prompt_tokens, response_tokens, total_tokens = summarizer.generate_summary(text_input, prompt_template, detail_level, audience)
            
            # Display the summary result
            if summary:
                st.success(f"{summary_type}:")
                st.write(f"**Word count of input text**: {word_count}")
                st.write(f"**Input text length**: {len(text_input)} characters")
                st.write(summary)
                word_count = len(summary.split())
                st.write(f"**Word Count**: {word_count}")
                st.write(f"**Length**: {len(summary)} characters")
                st.write(f"**Prompt tokens**: {prompt_tokens}")
                st.write(f"**Response tokens**: {response_tokens}")
                st.write(f"**Total tokens used**: {total_tokens}")
            else:
                st.error(f"{summary_type} failed.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
