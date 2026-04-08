---
title: RL Interview System
emoji: 💡
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# RL Interview System

A complete Reinforcement Learning-driven interview system that uses free Hugging Face LLMs to dynamically generate technical interview questions based on the candidate's evolving state metrics (technical knowledge, communication, confidence, and fatigue).

This system simulates an assessment engine where answers are auto-evaluated (simulated) and the LLM difficulty adjusts based on RL logic over an 8-question session.

## Components
*   `env/interview_env.py`: Reinforcement Learning environment maintaining candidate state and computing rewards.
*   `inference.py`: Dynamically streams contextual technical questions from the Hugging Face API.
*   `backend/main.py`: FastAPI server bridging the environment logic with REST APIs.
*   `static/`: Features a clean, responsive front-end UI.
*   `Dockerfile`: Container configuration targeting deployment.

## Installation & Running Locally

1. **Install Prerequisites**: Ensure you have Python 3.11 installed.
2. **Install Packages**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3. **Set Environment Variables**:
    *   `HF_TOKEN`: Your Hugging Face user token (Required)
    *   `MODEL_NAME`: (Optional) Free LLM model name, defaults to `openai/gpt-oss-20b`
    *   `API_BASE_URL`: (Optional) Defaults to `https://router.huggingface.co`

    *Windows (PowerShell)*:
    ```powershell
    $env:HF_TOKEN="your_token_here"
    ```

    *Linux/macOS*:
    ```bash
    export HF_TOKEN="your_token_here"
    ```

4. **Start the API Server**:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```
5. **Access Application**:
    Navigate to `http://localhost:8000/ui` in your web browser. 

## Docker & Deployment to Hugging Face Spaces

### Build and Run with Docker
```bash
docker build -t rl-interview .
docker run -p 8000:8000 -e HF_TOKEN="your_token_here" rl-interview
```

### Deploy to Hugging Face Spaces
This completely containerized architecture is built for Hugging Face Docker Spaces!
1. Go to Hugging Face -> New Space.
2. Select **Docker** as the Space SDK.
3. In the space Settings -> "Variables and secrets", add your Secret named `HF_TOKEN`.
4. Upload or push all project files, and the container will build and serve your app. *Note: If HF spaces complain about port 8000, you can adapt the EXPOSE inside the Dockerfile to 7860 and change the uvicorn port.*
