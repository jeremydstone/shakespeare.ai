from urllib import response
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from ollama import chat
from ollama import ChatResponse

MODEL_OLMO = 'olmo2:7b'
MODEL_LLAMA = 'llama3.2:1b'

INSULT_PROMPT = "Create a witty and humorous insult about me in the style of Shakespeare. "\
                "Make it clever and unique. Specifically insult my {insult_type}."

INSULT_TYPES = [
    "fashion sense",
    "inflated ego",
    "hair style",
    "intellect",
    "physical prowess",
    "social skills",
    "charisma",
    "cooking skills",
    "taste in LLMs"
]

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_exempt
def generate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    insult_id = int(request.POST.get("data", None))
    if insult_id is None:
        return JsonResponse({'error': 'No data provided'}, status=400)

    insult_type = INSULT_TYPES[insult_id]
    prompt = INSULT_PROMPT.format(insult_type=insult_type)

    response: ChatResponse = chat(model=MODEL_OLMO, messages=[
        {
            'role': 'user',
            'content': prompt
        },
    ])
  
    content = "On the subject of your " + insult_type + ", I must say:\n\n" + response.message.content

    return JsonResponse({"content": json.dumps(content), "prompt": json.dumps(prompt)}, status=200)