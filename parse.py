from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define prompt template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string (''). "
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Load Ollama Model
model = OllamaLLM(model="llama3")

def parse_with_ollama(dom_chunks, parse_description):
    """Extracts specific data from website content using Ollama LLM."""
    
    # Ensure parse description is provided
    if not parse_description.strip():
        return "Error: No parse description provided."

    # Create chain with input variables
    prompt = ChatPromptTemplate.from_template(template, input_variables=["dom_content", "parse_description"])
    chain = prompt | model

    parsed_results = []

    # Process each chunk
    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            print(f"[Batch {i}/{len(dom_chunks)}] Processing {len(chunk)} characters...")
            response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
            parsed_results.append(response)
        except Exception as e:
            print(f"⚠️ Error processing batch {i}: {e}")
            parsed_results.append(f"Error processing batch {i}: {str(e)}")

    return "\n".join(parsed_results)
