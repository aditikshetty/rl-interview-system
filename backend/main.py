import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Ensure parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.interview_env import InterviewEnv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = InterviewEnv()

# Pydantic Typing for models
class ResetRequest(BaseModel):
    task: Optional[str] = None

class ActionRequest(BaseModel):
    message: str

class Observation(BaseModel):
    echoed_message: str

class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict

class StateResponse(BaseModel):
    state: dict
    observation: Observation

@app.get("/")
def read_root():
    return {"message": "RL Interview Env Running", "status": "200 OK"}

@app.get("/state", response_model=StateResponse)
def get_state():
    obs = env._get_observation()
    return StateResponse(state=env.state, observation=Observation(echoed_message=obs["echoed_message"]))

@app.post("/reset", response_model=StateResponse)
def reset_env(req: Optional[ResetRequest] = None):
    task_name = req.task if req else None
    obs = env.reset(task=task_name)
    return StateResponse(state=env.state, observation=Observation(echoed_message=obs["echoed_message"]))

@app.post("/step", response_model=StepResponse)
def step_env(req: ActionRequest):
    obs, reward, done, info = env.step(req.message)
    return StepResponse(
        observation=Observation(echoed_message=obs["echoed_message"]),
        reward=reward,
        done=done,
        info=info
    )

# Mount static files folder
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/ui")
def read_ui():
    ui_path = os.path.join(static_dir, "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path)
    return {"error": "UI not found"}
