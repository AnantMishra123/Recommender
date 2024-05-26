import os
from dotenv import load_dotenv
from groq import Groq
import json

# Load .env file
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "keywords": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["keywords"]
}

# Convert the schema to a JSON string
schema_str = json.dumps(schema, indent=2)

def get_keywords(prompt:str):
    valid=True
    while(valid):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                    "role": "system",
                    "content": "You are designed to generate movie keywords given a situation."
                                f" The JSON object must use the schema: {schema_str}"
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}",
                    }
                ],
                model="llama3-8b-8192",
                response_format={"type": "json_object"},
            )
            valid=False
        except Exception as e:
            valid=True
    return chat_completion.choices[0].message.content

