# Hi_LLM_Chat

# 💬 Hi_LLM_Chat: 로컬에서 즐기는 Llama 3.2 1B 기반 멀티턴 챗봇

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) **Hi_LLM_Chat**은 여러분의 컴퓨터에서 직접 실행되는 간단하면서도 강력한 멀티턴(multi-turn) 챗봇입니다. 최신 **Llama 3.2 1B 모델**을 기반으로 하며, 사용자와의 자연스러운 대화를 목표로 합니다. 특히, **실시간 스트리밍** 응답 생성을 통해 마치 실제 대화처럼 텍스트가 나타나는 것을 경험할 수 있습니다! 🚀

## ✨ 주요 특징

* **🖥️ 100% 로컬 실행:** 인터넷 연결 없이, 외부 API 호출 없이 사용자의 PC에서 모든 것이 처리됩니다. (모델 다운로드 제외)
* **🔄 멀티턴 대화 지원:** 이전 대화 내용을 기억하여 문맥에 맞는 응답을 생성합니다.
* **🦙 Llama 3.2 1B 모델 활용:** 비교적 가벼우면서도 준수한 성능의 최신 언어 모델을 사용합니다.
* **💨 실시간 스트리밍 응답:** 챗봇의 답변이 타이핑되듯 실시간으로 표시되어 지루할 틈이 없습니다.
* **🔧 간단한 구조:** 핵심적인 챗봇 기능에 집중하여 이해하고 수정하기 용이합니다.

## 🎬 데모 (선택 사항)

(여기에 챗봇이 실제로 작동하는 모습의 GIF나 스크린샷을 추가하면 좋습니다!)

![Demo GIF Placeholder](https://via.placeholder.com/600x300.png?text=Chatbot+Demo+GIF+Here)

## ⚙️ 요구 사항

* **Python:** 3.8 이상 버전 권장
* **필수 라이브러리:** (프로젝트에 사용된 라이브러리를 `requirements.txt` 파일에 명시하고 아래에 간략히 언급)
    * `llama-cpp-python` (또는 `transformers` 등 모델 로딩 및 추론 라이브러리)
    * 기타 필요한 라이브러리 (예: `streamlit`, `flask` 등 UI 관련 라이브러리)
* **Llama 3.2 1B 모델:** GGUF 형식의 모델 파일 (llama-cpp-python 사용 기준)
* **하드웨어:**
    * 적절한 성능의 CPU
    * 충분한 RAM (최소 8GB 이상 권장, 모델 크기에 따라 다름)
    * (선택) GPU 가속을 위한 호환 가능한 GPU 및 CUDA/ROCm 설정 (llama-cpp-python 설정에 따라)

## 🛠️ 설치 방법

1.  **저장소 복제:**
    ```bash
    git clone [https://github.com/YourUsername/Hi_LLM_Chat.git](https://www.google.com/search?q=https://github.com/YourUsername/Hi_LLM_Chat.git)  # YourUsername을 실제 GitHub 사용자 이름으로 변경하세요
    cd Hi_LLM_Chat
    ```

2.  **필수 라이브러리 설치:**
    ```bash
    pip install -r requirements.txt # requirements.txt 파일이 필요합니다.
    ```
    * `llama-cpp-python` 설치 시 GPU 지원이 필요하면 해당 라이브러리 문서를 참고하여 빌드 옵션을 지정하세요.

4.  **Llama 3.2 1B 모델 다운로드:**
    * Hugging Face Hub 등 신뢰할 수 있는 출처에서 **Llama 3.2 1B 모델의 GGUF 형식 파일**을 다운로드합니다. (예: `llama-3.2-1b.Q4_K_M.gguf`)
    * 다운로드한 모델 파일을 프로젝트 내 특정 폴더(예: `./models`)에 위치시킵니다.
    * **주의:** 모델 라이선스를 반드시 확인하고 준수하세요.

5.  **(필요시) 설정 업데이트:**
    * 코드 내(예: `config.py` 또는 메인 스크립트)에서 다운로드한 모델 파일의 경로가 올바르게 지정되었는지 확인하고 필요하면 수정합니다.

## ▶️ 실행 방법

1.  터미널에서 다음 명령어를 실행합니다:
    ```bash
    python main.py  # 또는 실제 실행 스크립트 이름
    ```
2.  챗봇이 실행되면 프롬프트에 메시지를 입력하고 Enter 키를 누릅니다.
3.  챗봇이 생성하는 응답이 스트리밍 방식으로 출력되는 것을 확인합니다.

## 🧠 모델 정보

* **기반 모델:** Meta의 Llama 3.2 (1B 파라미터 버전)


## 🔧 설정 (선택 사항)

코드 내에서 모델 경로, 생성 파라미터(temperature, top_p 등), 최대 토큰 수 등을 조절할 수 있습니다. (구체적인 설정 방법을 여기에 추가)
