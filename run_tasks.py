import argparse
import sys
from env.interview_env import InterviewEnv

def main():
    env = InterviewEnv()
    
    tasks = ["python_task", "sql_task", "system_design_task"]
    
    for task_name in tasks:
        print(f"========================================")
        print(f"Running Task: {task_name}")
        obs = env.reset(task=task_name)
        done = False
        print(f"Initial Observation: {obs['echoed_message']}")
        
        while not done:
            # Provide a dummy simulated valid response
            if task_name == "python_task":
                answer = "Here is my answer: def generate(): yield 1"
            elif task_name == "sql_task":
                answer = "Here is my answer: select max(salary) limit 1 offset 1"
            else:
                answer = "Here is my answer: caching, load balancer, hash, database"
                
            obs, reward, done, info = env.step(answer)
            print(f"- step | reward: {reward:.2f} | score: {env.state['technical_score']:.2f} | q_asked: {env.state['questions_asked']}")
            
        print(f"Finished {task_name}! Final Score: {env.state['technical_score']}")
        print(f"========================================\n")

if __name__ == "__main__":
    main()
