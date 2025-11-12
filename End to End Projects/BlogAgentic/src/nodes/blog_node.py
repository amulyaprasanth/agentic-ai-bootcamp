from src.states.blog_state import BlogState, Blog

class BlogNode:
    """A class to represent the blog node."""
    
    def __init__(self, llm):
        self.llm = llm
        
    def title_creation(self, state: BlogState):
        """Create a title for the blog."""
        if "topic" in state and state["topic"]:
            prompt = (
                "You are an expert blog content writer. Use markdown formatting. "
                "Generate a blog title for the {topic}. This title should be creative and SEO friendly."
            )
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            # Return proper Blog object
            return {
                "blog": Blog(
                    title=response.content.strip(),
                    content=""
                )
            }

    def content_generation(self, state: BlogState):
        """Generate detailed blog content."""
        if "topic" in state and state["topic"]:
            system_prompt = (
                "You are an expert blog writer. Use markdown formatting. "
                "Generate a detailed blog content with a detailed breakdown of the {topic}."
            )
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            # Return proper Blog object using existing title
            return {
                "blog": Blog(
                    title=state["blog"].title,
                    content=response.content.strip()
                )
            }
