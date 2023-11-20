#!/usr/bin/env python3
import openai
import argparse

from typing import List
from APIKEY import API_KEY

openai.api_key = API_KEY
TOKEN_LIMIT = 500
END_WORDS = [ 'done', 'stop', 'end', 'quit', 'exit']
EXPERTS = [ 'haberdasher', 'sommelier', 'gouda person']

def user_input() -> str:
    print("> ",end='')
    return input()

def chat(model: str, tokens: int, system_prompt: str, verbose: bool = False):
    print("Please enter your question or type 'Done' when Done or reset for a new chat.")

    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input()})
    
    while (messages[-1]["content"].lower() not in END_WORDS):
        response = openai.chat.completions.create(
            model=model,
            messages = messages,
            max_tokens=tokens,
        )
        print(response.choices[0].message.content)
        if verbose:
            print("Usage: ", response.usage)

        newinput = user_input()
        if newinput.lower() == 'reset':
            messages = [
                    {"role": "system", "content": system_prompt}
            ]
            print("New chat begins.")
            print("================")
            newinput = user_input()

        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content,
        })
        messages.append({
            "role": "user",
            "content": newinput,
        })
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model',help="name of model to use",default='gpt-4-1106-preview')
    parser.add_argument('-t','--tokens',help="token limit suggestion",default=TOKEN_LIMIT)
    parser.add_argument('-p','--prompt',help="system propt such as you are a helpful assistant", default="you are an expert " + EXPERTS[random.randint(len(EXPERTS)))
    parser.add_argument('-l','--list-models',help="List models instead of querying one", action='store_true')
    parser.add_argument('-v','--verbose',help="print additional output", action='store_true')
    args = parser.parse_args()

    if args.list_models:
        print("Attempting to list models:")
        client = openai.OpenAI(
            api_key = API_KEY,
                )
        for model in client.models.list():
            print(model.id)
    else:
        print(f"Starting chat with model {args.model}.")
        chat(args.model,args.tokens,args.prompt, args.verbose)

if __name__=='__main__':
    main()