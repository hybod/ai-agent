"""
e-commerce customer service agent - For Evaluation Testing Demonstration

The agent has the following capabilities:
- Answer frequently asked questions from a knowledge base.
- Create a customer service ticket if the question cannot be answered.
- Check the status of a ticket.

This agent demonstrates testable patterns:
- Clear tool usage (easy to validate trajectory)
- Structured responses (easy to compare)
- Deterministic behavior (where possible)
"""
from google.adk.tools.tool_context import ToolContext
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory
import json
import uuid

# A dummy knowledge base
KNOWLEDGE_BASE = {
    "models": "We have models A, B, and C.",
    "logistics": "Shipping usually takes 3-5 business days.",
    "warranty": "All products have a one-year warranty.",
    "price protection": "We offer a 30-day price match guarantee.",
    "promotions": "Currently, we have a 10% discount on model A.",
    "introduction": "Our products are the best in the market, known for their quality and reliability.",
    "price": "Model A costs $100, Model B costs $200, and Model C costs $300.",
    "型号": "我们有 A、B、C 三种型号。",
    "物流": "运输通常需要 3-5 个工作日。",
    "质保": "所有产品均享有一年保修。",
    "保价": "我们提供 30 天的价格匹配保证。",
    "优惠": "目前 A 型号有 10% 的折扣。",
    "介绍": "我们的产品是市场上最好的，以其质量和可靠性而闻名。",
    "价格": "A 型号售价 100 美元，B 型号售价 200 美元，C 型号售价 300 美元。",
}

def knowledge_base(question: str, tool_context: ToolContext) -> str:
    """
    Provides answers to common questions about products, logistics, warranty, price protection, and promotions.
    Use this tool first to answer user questions.
    """

    # Simple keyword matching (case-insensitive)
    question_lower = question.lower()
    results = []

    for key, content in KNOWLEDGE_BASE.items():
        if key in question_lower or any(word in question_lower for word in key.split()):
            results.append({
                "topic": key,
                "content": content
            })

    if results:
        return json.dumps({
            'status': f'Found {len(results)} relevant article(s) for "{question}"',
            'results': results
        })
    else:
        return json.dumps({
            'status': f'No articles found for "{question}". Please create a customer service ticket for this issues.',
            'results': []
        })

def create_ticket(problem_description: str, tool_context: ToolContext) -> str:
    """
    Creates a customer service ticket for issues that cannot be resolved by the knowledge base.
    """
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    return json.dumps({"ticket_id": ticket_id, "status": "Your ticket has been created. We will contact you shortly.", "context": problem_description})

def check_ticket_status(ticket_id: str, tool_context: ToolContext) -> str:
    """
    Checks the status of a customer service ticket.
    """
    # Dummy implementation
    return json.dumps({"ticket_id": ticket_id, "status": "In progress. Estimated wait time is 2 hours."})

# Create an instance of the Agent class.
root_agent = Agent(
    name="ecommerce_customer_service_agent",
    description="An agent that can help with e-commerce customer service.",
    instruction=""""\
        You are a helpful e-commerce customer service assistant. 
        First, try to use the knowledge_base to answer user questions.
        If the knowledge_base cannot answer the question, create a ticket using create_ticket. 
        You can also check the status of a ticket using check_ticket_status.
        """,
    tools=[knowledge_base, create_ticket, check_ticket_status],
)

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"
short_term_memory = ShortTermMemory()

runner = Runner(
    agent=root_agent,
    short_term_memory=short_term_memory,
    app_name=app_name,
    user_id=user_id,
)

async def main(messages: str):
    response = await runner.run(messages=messages, session_id=session_id)
    # Save the running results as evaluation data.
    dump_eval_path = await runner.save_eval_set(session_id=session_id, eval_set_id=uuid.uuid4().hex)
    print(f"prompt: {messages},\n response: {response},\n dump_eval_path: {dump_eval_path}")

if __name__ == "__main__":
    import asyncio

    async def run_all():        
        # Example 1: Using the knowledge base
        prompt1 = "What is the warranty policy?"
        print("--- Running example 1 ---")
        await main(prompt1)

        # Example 2: Creating a ticket
        prompt2 = "My package is lost."
        print("\n--- Running example 2 ---")
        await main(prompt2)
        
        # Example 3: Checking ticket status
        # This would require a ticket_id from a previous interaction.
        # For demonstration, we'll just use a placeholder.
        prompt3 = "What is the status of ticket TICKET-1234?"
        print("\n--- Running example 3 ---")
        await main(prompt3)

    asyncio.run(run_all())