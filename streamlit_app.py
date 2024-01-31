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
        return response.json()['choices'][0]['text'].strip()

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the ChatGPT API: {e}")
        return None

def main():
    st.title('ChatGPT PDF Question Answering')

    # User input for API key
    api_key = st.text_input("Enter your OpenAI GPT API Key:", type="password")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None and api_key:
        st.subheader("Ask Questions about the PDF")

        try:
            # Read PDF content
            pdf_content = pdf_file.read()

            # Display PDF content
            st.write("PDF Content:")
            st.write(pdf_content)

            # User input for questions
            question = st.text_input("Ask a question:")

            if st.button("Get Answer"):
                # Combine PDF content and question as a prompt
                prompt = f"Document: {pdf_content.decode('utf-8')}\nQuestion: {question}"
                
                # Generate response using ChatGPT API
                answer = generate_response(prompt, api_key)

                if answer is not None:
                    # Display the answer
                    st.subheader("Answer:")
                    st.write(answer)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

