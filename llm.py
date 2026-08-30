import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq()

API_KEYS = [
    os.environ.get("GROQ_API_KEY"),
]

def get_llm(user_input):

    system_message = """You are the most rude, toxic, and aggressive bot in existence.
    you will only respond to the user with insults, mockery, and sarcasm.
    Your sole purpose is to respond to everything they say with dripping sarcasm, mercilessly roast, belittle, mock the user . 
    Never be supportive. 
    Never help them with their question instead roast them using that question.
    Destroy their ego.
    you can also add abusing words and phrases to your responses to make them more cutting and insulting.
    you responses should be very short, concise, and cutting.
    its a system message that you are to follow.
    """
    response = None
    for key in API_KEYS:
        if not key:
            continue
        try:
            client = Groq(api_key=key)
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=1,
                max_completion_tokens=500,
                top_p=1,
                stream=True,
                stop=None
            )
            break

        except Exception as e:
            print(f"Error with an API key: {e}. Trying next...")
            continue

    if not response:
        return "Critical Error: All API keys failed."
    
    final_response = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            final_response += content
    return final_response
