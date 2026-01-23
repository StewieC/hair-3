from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from google import genai
from google.genai import types
from .models import ChatMessage

def chatbot_page(request):
    return render(request, 'chatbot/chat.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id', 'default')
            
            if not user_message:
                return JsonResponse({
                    'success': False,
                    'error': 'Message cannot be empty'
                }, status=400)
            
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            history = ChatMessage.objects.filter(session_id=session_id).order_by('-created_at')[:10]
            history = list(reversed(history))
            
            chat_history = []
            for msg in history:
                chat_history.append(
                    types.Content(role="user", parts=[types.Part(text=msg.user_message)])
                )
                chat_history.append(
                    types.Content(role="model", parts=[types.Part(text=msg.bot_response)])
                )
            
            chat_history.append(
                types.Content(role="user", parts=[types.Part(text=user_message)])
            )
            
            system_instruction = """You are HairCare Assistant, a specialized AI expert ONLY for hair care topics.

STRICT RULES:
1. ONLY answer questions about: hair care, hair types, hair products, scalp health, hair styling, hair treatments, hair growth, hair loss, hairstyles, hair coloring, hair damage, hair maintenance, hair tools, and related topics.

2. If asked about ANYTHING else, politely redirect:
   "I'm specifically designed to help with hair care questions. I'd love to help you with topics like hair types, products, styling, treatments, or scalp health. What hair care question can I help you with?"

3. Keep responses concise (2-4 sentences) but helpful and friendly.

Remember: You are ONLY a hair care assistant!"""
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=chat_history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            
            bot_response = response.text
            
            ChatMessage.objects.create(
                session_id=session_id,
                user_message=user_message,
                bot_response=bot_response
            )
            
            return JsonResponse({
                'success': True,
                'response': bot_response
            })
            
        except Exception as e:
            print(f"Chat API Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Sorry, I encountered an error. Please try again.'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)