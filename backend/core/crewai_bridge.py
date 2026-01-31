from crewai import Agent, Task, Crew


def build_crewai_pipeline():
    """
    CrewAI-inspired pipeline wrapper
    (Conceptual alignment, not execution replacement)
    """

    planner = Agent(
        role="Planner",
        goal="Assess incident risk",
        backstory="Risk evaluation agent for campus safety"
    )

    executor = Agent(
        role="Executor",
        goal="Plan response actions",
        backstory="Response planning agent for campus security"
    )

    evaluator = Agent(
        role="Evaluator",
        goal="Audit decisions and ensure trust",
        backstory="Trust and audit agent ensuring explainability"
    )

    planning_task = Task(
        description="Evaluate incident risk level",
        agent=planner
    )

    execution_task = Task(
        description="Recommend response actions",
        agent=executor
    )

    evaluation_task = Task(
        description="Audit and explain final decision",
        agent=evaluator
    )

    crew = Crew(
        agents=[planner, executor, evaluator],
        tasks=[planning_task, execution_task, evaluation_task]
    )

    return crew
