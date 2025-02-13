from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import send_email,send_registeration_email
# Create your views here.


def process_data(request):
    if request.method == "POST":
        data = eval(request.body.decode('utf-8'))
        try:
            send_email.delay(data['email'],data['name'],data['url'],data['template'],data['subject'],data['company_name'],data['msg'])
        except Exception as e:
            return JsonResponse({"status":500,"message":"email not sent "})
    return JsonResponse({"status":200,"message":"email sent successfully"})



import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.tasks import send_registeration_email  # Importing the Celery task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@csrf_exempt
def Register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            logger.info(f"Received registration request: {data}")

            # Validate required keys
            required_keys = ['recipient_email', 'name', 'subject', 'organizer', 'start_date', 'start_time', 'location', 'event_name']
            if not all(key in data for key in required_keys):
                logger.error("Missing required fields in request data")
                return JsonResponse({"status": 400, "message": "Missing required fields"}, status=400)

            # Send email via Celery
            send_registeration_email.delay(
                data['recipient_email'],
                data['name'],
                data['subject'],
                data['organizer'],
                data['start_date'],
                data['start_time'],
                data['location'],
                data['event_name']
            )
            logger.info("Email task dispatched successfully")
            return JsonResponse({"status": 200, "message": "Email sent successfully"})

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {str(e)}")
            return JsonResponse({"status": 400, "message": "Invalid JSON format"}, status=400)

        except Exception as e:
            logger.exception("Error while sending email")
            return JsonResponse({"status": 500, "message": "Email not sent due to an internal error"}, status=500)

    logger.warning("Invalid request method used")
    return JsonResponse({"status": 405, "message": "Method Not Allowed"}, status=405)
