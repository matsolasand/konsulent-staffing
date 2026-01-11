import requests
import json
import time

k = "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"
OPENROUTER_API_KEY = k
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define your tool (your API)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_available_consultants",
            "description": "Get summary of available consultants with specific skills",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_tilgjengelige_prosent": {
                        "type": "integer",
                        "description": "Minimum availability percentage required",
                        "minimum": 1,
                        "maximum": 100
                    },
                    "pakrevd_ferdighet": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of required skills",
                        "enum": ["python", "c++", "java", "fortran", "fullstack"]
                    }
                    # "pakrevd_ferdighet": {
                    #     "type": "string",
                    #     "description": "Required skill",
                    #     "enum": ["python", "c++", "java", "fortran", "fullstack"]
                    # }
                },
                "required": ["min_tilgjengelige_prosent", "pakrevd_ferdighet"]
            }
        }
    }
]

def call_openrouter(model, messages, tools=None):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    # Only add tools if provided
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"  # Let model decide when to use tools
    
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    return response.json()

def call_your_api(min_tilgjengelighet_prosent, pakrev_ferdighet):
    url = "http://localhost:8001/tilgjengelige-konsulenter/sammendrag?"\
        + "min_tilgjengelighet_prosent=50&pakrevde_ferdigheter=python&"\
        + "pakrevde_ferdigheter=c%2B%2B"
    params = {
        "min_tilgjengelighet_prosent": min_tilgjengelighet_prosent,
        "pakrevd_ferdighet": pakrev_ferdighet
    }
    response = requests.get(url, params=params)
    return response.json()




def main():
    def models(num):
        """
        Fast, cheap, and excellent at structured outputs.
        """
        if num == 0:
            model = "anthropic/claude-3.5-haiku"
        elif num == 1:
            model = "openai/gpt-4o-mini"
        elif num == 2:
            model = "openai/gpt-3.5-turbo"
        if num == 3:
            # works, despite failed type correctness
            model = "meta-llama/llama-3.1-8b-instruct"
        return model
    
    boolt, boolf = (True, False)
    messages = [
        {
            "role": "user",
            "content": "Find me developers with both Python and c++ and at least 50% availability"
            # "content": "Find me Python developers with at least 50% availability"
        }
    ]
    ############
    # parameters
    ############
    # choose one out of four models (kwarg in [0, 1, 2, 3])
    model = models(0)
    # prints result from call_openrouter() if True
    testing_output = boolf
    ############
    start = time.time()
    result = call_openrouter(
        model = model,
        messages = messages,
        tools = tools
    )
    print(type(result))
    elapsed = time.time() - start
    print(f"Response time: {elapsed:.2f}s")
    if testing_output:
        print(result)
        return
    tool_call = result['choices'][0]['message']['tool_calls'][0]
    args = json.loads(tool_call['function']['arguments'])

    api_result = call_your_api(
        args['min_tilgjengelige_prosent'],
        args['pakrevd_ferdighet']
    )
    print(api_result)

if __name__ == "__main__":
    main()


"""
Example call for call_openrouter():

result = call_openrouter(
    model=model,
    messages=messages,
    tools=tools
)

Response structure:

{
    "choices": [{
        "message": {
            "role": "assistant",
            "content": null,  # null when using function call
            "tool_calls": [{
                "function": {
                    "name": "get_available_consultants",
                    "arguments": "{\"min_tilgjengelighet_prosent\": 60, \"pakrevd_ferdighet\": \"python\"}"
                }
            }]
        }
    }]
}

"""