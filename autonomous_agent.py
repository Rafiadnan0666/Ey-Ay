import asyncio
import json
from ollama_integration import get_ollama_response
import actions

class AutonomousAgent:
    def __init__(self, conversation_history):
        self.conversation_history = conversation_history

    async def run(self, initial_prompt):
        self.conversation_history.append({"role": "user", "content": initial_prompt})
        
        while True:
            # Get the next action from the LLM
            llm_response = await asyncio.to_thread(
                get_ollama_response,
                "Given the conversation history, what is the next action to take?",
                conversation_history=self.conversation_history
            )

            try:
                parsed_response = json.loads(llm_response)
                action = parsed_response.get("action")
                arguments = parsed_response.get("argument")
                reasoning = parsed_response.get("reasoning")
                task_complete = parsed_response.get("task_complete")

                if task_complete:
                    print(f"Task complete: {reasoning}")
                    self.conversation_history.append({"role": "assistant", "content": f"Task complete: {reasoning}"})
                    return reasoning

                if hasattr(actions, action):
                    action_func = getattr(actions, action)
                    
                    # Execute the action
                    if asyncio.iscoroutinefunction(action_func):
                        response = await action_func(**arguments)
                    else:
                        response = await asyncio.to_thread(action_func, **arguments)
                    
                    print(f"Action: {action}, Arguments: {arguments}, Response: {response}")
                    
                    # Update conversation history
                    self.conversation_history.append({"role": "assistant", "content": f"Action: {action}, Response: {response}"})
                else:
                    print(f"Unknown action: {action}")
                    self.conversation_history.append({"role": "assistant", "content": f"Unknown action: {action}"})
                    break

            except json.JSONDecodeError:
                print(f"Invalid JSON response from LLM: {llm_response}")
                self.conversation_history.append({"role": "assistant", "content": f"Invalid JSON response: {llm_response}"})
                break
