from app.bob_integration.prompt_engine import build_prompt
from app.bob_integration.bob_adapter import BobAdapter

class BobClient:
    def __init__(self):
        self.adapter = BobAdapter()

    def query(self, mode: str, user_input: str, context: dict = None):
        prompt = build_prompt(mode, user_input, context)

        response = self.adapter.run(prompt)

        return {
            "mode": mode,
            "prompt_used": prompt,
            "bob_response": response
        }
