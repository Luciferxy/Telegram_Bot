
Telegram AI Email Bot 🤖📧


A Telegram bot powered by CrewAI and Composio-CrewAI that takes simple inputs from users, writes professional emails, and sends them to the requested recipient's email address.

## ✨ Features


Natural Language Input: Users can send a message in plain English (e.g., "Send an email to john.doe@example.com about the project update and say 'The project is on track!'").

Professional Email Composition: The bot uses CrewAI to craft well-structured emails with proper greetings, body, and closing.

Gmail Integration: Emails are sent directly using Composio-CrewAI's Gmail tool.

Error Handling: The bot provides clear feedback if something goes wrong.

Tech Stack 🛠️
Python: The core programming language.

CrewAI: For AI-powered email writing.

Composio-CrewAI: For Gmail integration.

Telegram Bot API: For interacting with users on Telegram.

Ollama: For running the local LLM (e.g., llama3).
## ⚙️ Installation

Prerequisites
Python 3.8+: Ensure Python is installed on your system.

Telegram Bot Token: Create a bot using BotFather and get the token.

Composio API Key: Sign up at Composio and get your API key.

Ollama: Install and run Ollama locally to use the llama3 model.

Clone the repository:

bash
Copy
git clone https://github.com/your-username/telegram-ai-email-bot.git
cd telegram-ai-email-bot
Install dependencies:

bash
Copy
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory.

Add the following variables:

plaintext
Copy
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
COMPOSIO_API_KEY=your_composio_api_key
Run the bot:

bash
Copy
python telegram_bot.py
    
## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.




## 🙏 Acknowledgments
Acknowledgments 🙏
CrewAI: For the AI-powered email writing capabilities.

Composio-CrewAI: For seamless Gmail integration.

Ollama: For providing the local LLM (llama3).



