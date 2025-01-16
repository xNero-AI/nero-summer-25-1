from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import get_trends, get_serper_and_scrapping, create_newsletter

def compile_workflow():
    """ 
    Compiles the workflow for creating a newsletter from Google Trends.
    
    Returns:
        app (StateGraph): The compiled workflow.
    """
    
    # Define the graph
    workflow = StateGraph(GraphState)
    
    # Define the nodes
    workflow.add_node("get_trends", get_trends)
    workflow.add_node("get_serper_and_scrapping", get_serper_and_scrapping)
    workflow.add_node("create_newsletter", create_newsletter)

    # Build graph
    workflow.set_entry_point('get_trends')
    workflow.add_edge("get_trends", "get_serper_and_scrapping")
    workflow.add_edge("get_serper_and_scrapping", "create_newsletter")
    workflow.add_edge("create_newsletter", END)

    # Compile
    app = workflow.compile()
    return app