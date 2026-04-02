from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# 1. Local LLM (Ollama)
llm = Ollama(model="llama3.1")

# 2. Agents
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

# 3. Tasks
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

# 4. Crew (CRITICAL)
crew = Crew(
    agents=[developer, qa_engineer, reviewer],
    tasks=[task_write_code, task_debug_code, task_validate_code],
    llm=llm,          # ⭐ REQUIRED (prevents OpenAI fallback)
    verbose=True
)

# 5. Run
result = crew.kickoff()
print("\nFinal Output:\n")
print(result)
