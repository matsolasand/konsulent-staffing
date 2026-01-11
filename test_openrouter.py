import requests
import json

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
                        "type": "string",
                        "description": "Required skill",
                        "enum": ["python", "c++", "java", "fortran", "fullstack"]
                    }
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
    url = "http://localhost:8001/tilgjengelige-konsulenter/sammendrag"
    params = {
        "min_tilgjengelighet_prosent": min_tilgjengelighet_prosent,
        "pakrevd_ferdighet": pakrev_ferdighet
    }
    response = requests.get(url, params=params)
    return response.json()




def main():
    def bad_models(num):
        if num == 0:
            model = ""
        elif num == 1:
            model = ""
        elif num == 2:
            model = ""
        return model
    
    def good_models(num):
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
            model = "meta-llama/llama-3.1-8b-instruct"
        return model
    
    boolt, boolf = (True, False)
    messages = [
        {
            "role": "user",
            "content": "Find me Python developers with at least 50% availability"
        }
    ]
    ############
    # parameters
    ############
    good_model = boolf
    if good_model:
        model = good_models(2)
    else:
        model = bad_models(0)
    testing_output = boolf
    ############
    result = call_openrouter(
        model = model,
        messages = messages,
        tools = tools
    )
    if testing_output:
        print(result)
        return
    tool_call = result['choices'][0]['message']['tool_calls'][0]
    args = json.loads(tool_call['function']['arguments'])

    api_result = call_your_api(args['min_tilgjengelige_prosent'], args['pakrevd_ferdighet'])
    print(api_result)

if __name__ == "__main__":
    main()


"""
Example call for call_openrouter():

result = call_openrouter(
    model="anthropic/claude-3.5-haiku",  # or "openai/gpt-4o-mini"
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
"""
Needs more testing:

GPT-3.5 Turbo: Perfect execution
    Correct function call
    Correct parameter types (integer for min_tilgjengelige_prosent)
    Cost: $0.000111 (~5x cheaper than Claude Haiku)
    Fast

Tested models:

Llama 3.2 1B - Provider doesn't support function calling at all. Dead end.
Gemma 2B - Model doesn't exist on OpenRouter (wrong ID or not available).
Mistral 7B - Interesting failure:
    finish_reason: 'stop' - Finished normally (didn't use tool)
    content: '' - Returned empty string
    It ignored the function completely - Just gave up instead of calling
    the tool or responding with text
Llama 3.1 8B: Failed - Type error
    Called the function correctly BUT:
    "min_tilgjengelige_prosent": "50" - String instead of integer
    Your API expects an integer, this will likely cause an error
    Slower (627 prompt tokens vs 120 - inefficient prompt processing)
    Cheapest: $0.000067
"""