from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = Path(__file__).parent
pdf_path = str(SCRIPT_DIR / "docs/financial_report.pdf")
pdf_search_tool = PDFSearchTool(pdf=pdf_path)

@CrewBase
class Poc2PdfMultiagent():
    """Poc2PdfMultiagent crew"""

    agents_config = 'config/agents.yaml' 
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def pdf_rag_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['pdf_rag_agent'],
			tools=[pdf_search_tool],
			verbose=True
		)

    @agent
    def pdf_summary_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['pdf_summary_agent'],
			verbose=True
		)
    
    @agent
    def pdf_mcq_agent(self) -> Agent:
        return Agent(
			config=self.agents_config['pdf_mcq_agent'],
			verbose=True
		)

    @task
    def pdf_rag_task(self) -> Task:
        return Task(
			config=self.tasks_config['pdf_rag_task'],
		)


    @task
    def pdf_summary_task(self) -> Task:
        return Task(
			config=self.tasks_config['pdf_summary_task'],
		)
    
    @task
    def pdf_mcq_task(self) -> Task:
        return Task(
			config=self.tasks_config['pdf_mcq_task'],
		)

    @crew
    def crew(self) -> Crew:
        """Creates the Poc2PdfMultiagent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
