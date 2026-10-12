from dotenv import load_dotenv
import os

load_dotenv()

from anthropic import Anthropic

client = Anthropic()

resp = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Return a JSON object with fields: status, timestamp, and version."
                }
            ]
        }
    ]
)

print(resp.content[0].text)

