# Import the prompt string from prompt.py
from prompt import GLOBAL_PROMPT

# 1. Define the domain name you want to use
# You can get this value from a configuration file, user input, or any other source.
dynamic_domain = "Stock Market Analysis"

# 2. Use the .format() method to replace the placeholder
# The key inside .format() must match the placeholder name in the string (i.e., Domain_Name)
formatted_prompt = GLOBAL_PROMPT.format(Domain_Name=dynamic_domain)

# 3. Print the result to see the dynamically replaced prompt
print("--- Original Prompt ---")
print(GLOBAL_PROMPT)
print("\n--- Dynamically Formatted Prompt ---")
print(formatted_prompt)

# You can now use this 'formatted_prompt' variable in your agent's configuration.
# For example:
#
# from agent import agent
#
# agent.instruction = formatted_prompt