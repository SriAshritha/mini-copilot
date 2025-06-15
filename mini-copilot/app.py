import streamlit as st
from openai import OpenAI

# UI Setup
st.set_page_config(page_title="Mini Copilot", layout="wide")
st.title("🤖 Mini Copilot – Code & Doc Assistant")

# Input from user
task = st.selectbox("Choose a Task", [
    "Explain Code",
    "Add Comments to Code",
    "Write Test Cases",
    "Generate Documentation",
    "Ask Anything"
])

user_input = st.text_area("Enter your code or question here", height=250)

# Initialize OpenAI client
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.error("❌ OpenAI API key not found in secrets. Please add it to Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Optional: Display if API key loaded (for debug only; remove in production)
st.write("API Key Loaded:", bool(api_key))

def check_model_availability(model_name):
    try:
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        return model_name in model_ids
    except Exception as e:
        st.error(f"Error fetching model list: {e}")
        return False

selected_model = "gpt-3.5-turbo"  # safer default

if not check_model_availability(selected_model):
    st.warning(f"Model `{selected_model}` is not available with your API key. Please check your OpenAI account.")
    st.stop()

# Generate output
if st.button("Generate Response"):
    if not user_input.strip():
        st.warning("Please enter some code or a question.")
    else:
        prompt_map = {
            "Explain Code": f"Explain this code:\n{user_input}",
            "Add Comments to Code": f"Add detailed comments to this code:\n{user_input}",
            "Write Test Cases": f"Write test cases for this Python function:\n{user_input}",
            "Generate Documentation": f"Write documentation (docstring or markdown) for the following code:\n{user_input}",
            "Ask Anything": user_input
        }

        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are a helpful programming assistant."},
                        {"role": "user", "content": prompt_map[task]}
                    ]
                )
                result = response.choices[0].message.content
                st.markdown("### ✅ Copilot Response")
                st.code(result, language="python")
            except Exception as e:
                st.error(f"❌ Error from OpenAI API: {e}")
