from langgraph import LangGraph

class WebzinCreator:
    def __init__(self):
        self.graph = LangGraph(api_key="your-langgraph-api-key")

    def create_webzin(self, summaries):
        # Assume summaries is a list of summary strings
        webzin_html = self.graph.create_webzin(content=summaries)
        return webzin_html

# Example usage
graph = WebzinCreator()
summaries = ["Summary 1", "Summary 2", "Summary 3"]
webzin_html = graph.create_webzin(summaries)
print(webzin_html)
