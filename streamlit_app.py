import streamlit as st
import requests

def generate_response(prompt, api_key):
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        data = {
            'prompt': prompt,
            'max_tokens': 100,
        }

        response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', json=data, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        choices = response.json().get('choices', [])
        if choices:
            return choices[0].get('text', '').strip()
        else:
            return "No response from ChatGPT."

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the ChatGPT API: {e}")
        return None

def main():
    st.title('ChatGPT PDF Question Answering')

    # User input for API key
    api_key = st.text_input("Enter your OpenAI GPT API Key:", type="password")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Extra space for visual separation
    st.markdown("---")

    # User input for questions
    question = st.text_input("Ask a question:")

    # Always display the "Get Answer" button
    if st.button("Get Answer") and pdf_file is not None and api_key and question:
        # Cache PDF content
        pdf_content = pdf_file.read()

        st.subheader("Ask Questions about the PDF")

        # Display PDF content
        st.write("PDF Content:")
        st.text(pdf_content)

        # Combine PDF content and question as a prompt
        prompt = f"Document: {pdf_content.decode('utf-8', 'ignore')}\nQuestion: {question}"
        
        # Generate response using ChatGPT API
        answer = generate_response(prompt, api_key)

        # Display the answer
        st.subheader("Answer:")
        st.write(answer)

if __name__ == "__main__":
    main()


