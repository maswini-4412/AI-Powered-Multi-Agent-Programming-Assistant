from crewai import Agent, Task, Crew
from litellm import completion

# Custom wrapper CrewAI understands
class OllamaLLM:
    def __call__(self, messages, **kwargs):
        response = completion(
            model="ollama/llama3.1",
            messages=messages,
            api_base="http://localhost:11434"
        )
        return response["choices"][0]["message"]["content"]

llm = OllamaLLM()
    
# Agents
developer = Agent( 
    role="Developer",
    goal="Write correct Python code",
    backstory="You are a software developer who writes clean code.",
    llm=llm
)

qa_engineer = Agent(
    role="QA Engineer",
    goal="Find bugs and fix errors in the code",
    backstory="You are a QA engineer who checks code carefully.",
    llm=llm
)

reviewer = Agent(
    role="Reviewer",
    goal="Validate logic and approve final code",
    backstory="You are a senior engineer reviewing the solution.",
    llm=llm
)

# Tasks
task_write_code = Task(
    description="Write Python code to check whether a number is prime.",
    expected_output="Working Python code",
    agent=developer
)

task_debug_code = Task(
    description="Check the code for errors and fix them if needed.",
    expected_output="Error-free Python code",
    agent=qa_engineer
)

task_validate_code = Task(
    description="Validate the logic and confirm the code is correct.",
    expected_output="Approved final code",
    agent=reviewer
)

# Crew
crew = Crew(
    agents=[developer, qa_engineer, reviewer],
    tasks=[task_write_code, task_debug_code, task_validate_code],
    verbose=True
)

# Run
result = crew.kickoff()
print(result)
