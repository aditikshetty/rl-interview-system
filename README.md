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

## Deployment

This project is configured for automated deployment using GitHub Actions.

### 1. GitHub to Hugging Face Sync
The repository includes a GitHub Action ([sync_to_hf.yml](.github/workflows/huggingface_sync.yml)) that automatically pushes your code to Hugging Face Spaces whenever you push to the `master` branch.

**Setup Instructions:**
1.  **Hugging Face Token**: Generate a **Write** token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
2.  **GitHub Secrets**: In your GitHub repository, go to `Settings` -> `Secrets and variables` -> `Actions` and add a new secret:
    *   `HF_TOKEN`: Paste your Hugging Face Write token here.
3.  **Push to GitHub**: Once the secret is added, any push to the `master` branch will trigger the sync.

### 2. Manual Deployment to Hugging Face Spaces
If you prefer manual deployment:
1.  Create a new **Docker Space** on Hugging Face.
2.  In the Space **Settings**, add a **Secret** named `HF_TOKEN` (this is used by the application to access the LLM API).
3.  Upload the project files or use `git push` directly to the HF Space repository.

### 3. Docker Configuration
The `Dockerfile` is optimized for Hugging Face Spaces:
-   **Port**: Listens on `7860` (HF default).
-   **Base Image**: Lightweight `python:3.11-slim`.
-   **Streaming**: Supports real-time LLM interaction.

---
**Created by**: [Aditi Shetty](https://github.com/aditikshetty)
