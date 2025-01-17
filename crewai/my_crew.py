from crewai import Agent, Crew, Task, Process
from pydantic import BaseModel, Field
from typing import List
from crewai.project import CrewBase, crew, task, agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool


class NewsCollection(BaseModel):
    headline: str = Field(..., description="Título da noticia")
    link: str = Field(..., description="Link para noticia completa")
    preview: str = Field(..., description="Prévia da noticia")


class DetaliedNewsSummary(BaseModel):
    headline: str = Field(..., description="Título da noticia")
    news : List[NewsCollection] = Field(..., description="Lista de notícias")
    summary: str = Field(..., description="Resumo detalhado da noticia")
    link: str = Field(..., description="link para notícia completa")


class NewsSummary(BaseModel):
    news_summary: List[DetaliedNewsSummary] = Field(..., description="Lista de notícias sumarizadas")


@CrewBase
class NewsSummaryCrew():
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def coletor_de_noticias(self) -> Agent:
        return Agent(
            config=self.agents_config['coletor_de_noticia'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def sumarizador_de_noticias(self) -> Agent:
        return Agent(
            config=self.agents_config['sumarizador_de_noticia'],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def coleta_de_noticias_task(self) -> Task:
        return Task(
            config=self.tasks_config['coleta_de_noticias_task'],
            agent=self.coletor_de_noticias(),
        )

    @task
    def sumariza_noticia_task(self) -> Task:
        return Task(
            config=self.tasks_config['sumariza_noticia_task'],
            agent=self.sumarizador_de_noticias(),
            output_json=NewsSummary
        )

    @crew
    def crew(self) -> Crew:
        "Cria uma equipe de sumarizar noticias"
        
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process= Process.sequential,
            verbose = True
        )