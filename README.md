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
* **Llama 3.2 1B Model Weights & Tokenizer:** You need the official Llama 3.2 1B model weights and associated tokenizer files. Request access and download them from Meta's official channels: [https://llama.meta.com/llama-downloads/](https://llama.meta.com/llama-downloads/) (Follow the instructions on the site).

## 🛠️ Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/bok3948/Hi_LLM_Chat.git](https://github.com/bok3948/Hi_LLM_Chat.git)
    cd Hi_LLM_Chat
    ```

2.  **Download Model & Tokenizer:**
    * Obtain the Llama 3.2 1B (Instruct version recommended for chat) model weights and tokenizer from the official Meta channels (see Requirements).
    * Create a directory within the project to store the model files (e.g., `./llama3.2-1B-instruct/`).
    * Place all the downloaded model files (e.g., `consolidated.00.pth` or `.safetensors` files, `tokenizer.model`, `params.json`, or the relevant `.gguf` file if using llama.cpp) into the directory you created.
    * **Important:** You might need to update the model path in the configuration file or script (`config.py`, `chat.py`, etc.) to point to this directory.

3.  **Install Required Libraries:**
    ```bash
    pip install -r requirements.txt # Ensure you have this requirements.txt file
    ```
    * Note: If you need GPU support (e.g., for `llama-cpp-python`), refer to the specific library's documentation for installation options.

## ▶️ Usage

1.  **(Optional) Configure Model Settings:** Before running, you might need to adjust settings within the script or a configuration file (e.g., `config.py`, `chat.py`). For example, ensure options like `generate_full_logit` or KV cache are set according to your needs and the library used.

2.  **Run the Chatbot:** Open your terminal and execute the main script:
    ```bash
    python chat.py # Or the actual name of your execution script
    ```

3.  **Interact:** Once the chatbot starts, type your message into the prompt and press Enter.

4.  **Observe:** Watch as the chatbot's response is generated and displayed in a streaming fashion.

---
