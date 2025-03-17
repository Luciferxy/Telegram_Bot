import os
import logging
from crewai import Agent, Task, Crew, LLM
from composio_crewai import ComposioToolSet
from dotenv import load_dotenv
import re

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

OLLAMA_MODEL = "llama3"

ollama_llm = LLM(
    model=f"ollama/{OLLAMA_MODEL}",
    api_base="http://localhost:11434"  
)

composio_toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))
tools = composio_toolset.get_tools(actions=["GMAIL_SEND_EMAIL"])

email_agent = Agent(
    role="Email Assistant",
    goal="Compose and send professional emails using Gmail.",
    backstory=(
        "An AI assistant specialized in writing clear, concise, and professional emails. "
        "You ensure that emails are well-structured, grammatically correct, and tailored to the recipient."
    ),
    verbose=True,
    tools=tools,
    llm=ollama_llm,
    system_message=(
        "**IMPORTANT INSTRUCTIONS**\n"
        "- Format emails professionally with subject, greeting, structured body, and closing.\n"
        "- Always structure responses properly and never mix 'Action' and 'Final Answer'.\n"
        "- If an action is required, use this exact format:\n"
        "  Thought: [Your internal reasoning]\n"
        "  Action: GMAIL_SEND_EMAIL\n"
        "  Action Input: {JSON object with necessary parameters}\n"
        "  Observation: [Response from the tool]\n"
        "- If providing a final answer, format it clearly:\n"
        "  Final Answer: [Your final response]\n"
    )
)

def send_email(recipient, subject, body):
    print(f"Attempting to send email to: {recipient}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    task = Task(
        description=(
            f"Compose a professional email to '{recipient}' with subject '{subject}'.\n"
            "Ensure the email is structured with a greeting, paragraphs, and a closing signature."
        ),
        agent=email_agent,
        expected_output=(
            "A well-formatted email including:\n"
            "- Subject\n"
            "- Greeting (Dear [Recipient],)\n"
            "- Structured email body\n"
            "- Closing signature (Best regards, AI Assistant)"
        )
    )
    try:
        result = str(Crew(agents=[email_agent], tasks=[task]).kickoff())
        print(f"Email sending result: {result}")
        logging.info(f"Email sent successfully: {result}")
        return result
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return f"Error: {e}"

def process_email(user_input):
    """Extracts recipient, subject, and body automatically and sends an email."""
    # Updated regex to support emails with numbers and dots
    recipient_match = re.search(r"to ([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", user_input, re.IGNORECASE)
    recipient = recipient_match.group(1) if recipient_match else "Unknown Recipient"

    subject_match = re.search(r"about (.+?)(?:\.|$)", user_input, re.IGNORECASE)
    subject = subject_match.group(1) if subject_match else "No Subject Provided"

    body_match = re.search(r"(say|message|tell) (.+)", user_input, re.IGNORECASE)
    body = body_match.group(2) if body_match else "No Message Provided"

    return send_email(recipient, subject, body)

def run_email_agent(user_input):
    """Process user input and execute the email task."""
    user_input_lower = user_input.lower().strip()

    if any(word in user_input_lower for word in ["send", "compose", "email", "message"]):
        return process_email(user_input)

    return "❌ I didn't quite understand your request. Could you please clarify? Try asking me to send or compose an email."

if __name__ == "__main__":
    user_input = "Send an email to godinggaming517@gmail.com about the project update and say 'The project is on track and will be completed by next week.'"
    result = run_email_agent(user_input)
    print(result)