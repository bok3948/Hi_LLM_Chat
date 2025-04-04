# 💬 Hi_LLM_Chat: Your Local Multi-Turn Chatbot Powered by Llama 3.2 1B

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

**Hi_LLM_Chat** is a simple yet powerful multi-turn chatbot that runs entirely on your local machine. It's built upon the **Llama 3.2 1B model** and aims for natural conversations with users. Experience real-time interaction with its **streaming text generation** feature! 🚀

## ✨ Key Features

* **🖥️ 100% Local Execution:** No internet connection or external API calls needed (after model download). Everything is processed on your PC.
* **🔄 Multi-Turn Conversation Support:** Remembers previous parts of the conversation for contextual responses.
* **🦙 Utilizes Llama 3.2 1B Model:** Leverages a capable yet relatively lightweight large language model.
* **💨 Real-time Streaming Output:** Responses appear token-by-token, like someone typing in real-time, making interactions more engaging.
* **🔧 Simple Structure:** Focuses on core chatbot functionality, making it easy to understand and modify.

## 🎬 Demo (Optional)

*(Consider embedding or linking to a demo video showcasing the chatbot in action here.)*

## ⚙️ Requirements

* **Python:** 3.8+ recommended
* **Llama 3.2 1B Model Weights:** Download the official Llama 3.2 1B model weights. You may need to request access from Meta via their official channels: [https://llama.meta.com/llama-downloads/](https://llama.meta.com/llama-downloads/) (Follow the instructions on the site).
* **Llama 3.2 1B Tokenizer:** The tokenizer is typically included with the model download or can be obtained separately. Check the model source or documentation for details.

## 🛠️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/bok3948/Hi_LLM_Chat.git  # Change YourUsername to your actual GitHub username
    cd Hi_LLM_Chat
    ```

2.  **Install Required Libraries:**
    ```bash
    pip install -r requirements.txt # Ensure you have created this requirements.txt file
    ```
    * Note: If you need GPU support for `llama-cpp-python` or similar libraries, refer to their specific documentation for installation options.

## ▶️ Usage

1.  **(Optional) Configure Model Settings:** Before running, you might need to adjust model configurations (e.g., in `config.py` or the main script). For example, ensure settings like `generate_full_logit` or KV cache are enabled/disabled according to your needs and the library used.

2.  **Run the Chatbot:** Open your terminal and execute the main script:
    ```bash
    python chat.py  # Replace chat.py with the actual name of your execution script if different
    ```
3.  **Interact:** Once the chatbot is running, type your message into the prompt and press Enter.
4.  **Observe:** Watch as the chatbot's response is generated and displayed in a streaming fashion.

---
