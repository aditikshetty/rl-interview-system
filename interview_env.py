import numpy as np

class InterviewEnv:
    def __init__(self):
        self.max_questions = 8
        self.tasks = ["python_task", "sql_task", "system_design_task"]
        self.current_task = self.tasks[0]
        self.questions = {
            "python_task": "Write a Python generator that yields the Fibonacci sequence.",
            "sql_task": "Write a SQL query to find the second highest salary from an Employee table.",
            "system_design_task": "How would you design a scalable URL shortener like bit.ly?"
        }
        self.reset()
        
    def reset(self, task: str = None):
        if task in self.tasks:
            self.current_task = task
        else:
            self.current_task = "python_task"
            
        self.state = {
            "technical_score": 0.0,
            "fatigue": 0.0,
            "questions_asked": 0,
            "current_task": self.current_task
        }
        self.asked_questions_text = []
        return self._get_observation()
        
    def step(self, action_message: str):
        self.state["questions_asked"] += 1
        
        # Simple heuristic grader based on length and keywords to avoid using external API in env logic
        reward, tech_gain = self._grade_response(action_message, self.current_task)
        
        self.state["technical_score"] = min(1.0, max(0.0, self.state["technical_score"] + tech_gain))
        self.state["fatigue"] = min(1.0, self.state["fatigue"] + 0.1)
        
        done = self.state["questions_asked"] >= self.max_questions
        
        # Return structured observation, reward, done
        return self._get_observation(), float(reward), done, {"difficulty": "medium"}

    def _get_observation(self):
        if self.state["questions_asked"] >= self.max_questions:
            msg = "Interview complete."
        else:
            msg = self.questions[self.current_task]
            
        return {
            "echoed_message": msg,
            "state": self.state
        }
        
    def _grade_response(self, text: str, task: str) -> tuple[float, float]:
        text = text.lower()
        score = 0.0
        
        if len(text) > 20: 
            score += 0.1
            
        if task == "python_task":
            if "yield" in text: score += 0.6
            if "def" in text: score += 0.2
        elif task == "sql_task":
            if "select" in text: score += 0.4
            if "max" in text or "limit" in text or "offset" in text: score += 0.4
        elif task == "system_design_task":
            if "database" in text or "cache" in text: score += 0.4
            if "load balancer" in text or "hash" in text: score += 0.4
            
        final_reward = min(1.0, score)
        return final_reward, final_reward * 0.5
