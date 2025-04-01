import requests
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from homepro import settings
from datetime import datetime
from .models import MpesaTransaction

def subscribe(request):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer'+' '+settings.BEARER_KEY,

    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": settings.MPESA_PASSWORD,
        "Timestamp": "20250401135218",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254707485760,
        "PartyB": 174379,
        "PhoneNumber":254703443827,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload  # Use `json` instead of `data` for proper JSON formatting
    )

    try:
        response_data = response.json()  # Convert response to JSON
    except ValueError:
        response_data = {"error": "Invalid response from Safaricom API"}

    return JsonResponse(response_data)  # Return JSON response to the frontend


# Disable CSRF for this endpoint
@csrf_exempt
def mpesa_callback(request):
    pass
    # if request.method == "POST":
    #     try:
    #         mpesa_response = json.loads(request.body)
    #         print("M-Pesa Callback Received:", mpesa_response)  # Debugging

    #         stk_callback = mpesa_response.get('Body', {}).get('stkCallback', {})
    #         merchant_request_id = stk_callback.get('MerchantRequestID')
    #         checkout_request_id = stk_callback.get('CheckoutRequestID')
    #         result_code = stk_callback.get('ResultCode')
    #         result_desc = stk_callback.get('ResultDesc')
    #         callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])

    #         # Initialize fields
    #         amount = None
    #         mpesa_receipt_number = None
    #         transaction_date = None
    #         phone_number = None

    #         # Extract values
    #         for item in callback_metadata:
    #             if item["Name"] == "Amount":
    #                 amount = item["Value"]
    #             elif item["Name"] == "MpesaReceiptNumber":
    #                 mpesa_receipt_number = item["Value"]
    #             elif item["Name"] == "TransactionDate":
    #                 transaction_date = datetime.strptime(str(item["Value"]), "%Y%m%d%H%M%S")
    #             elif item["Name"] == "PhoneNumber":
    #                 phone_number = str(item["Value"])

    #         # Save transaction
    #         MpesaTransaction.objects.create(
    #             merchant_request_id=merchant_request_id,
    #             checkout_request_id=checkout_request_id,
    #             result_code=result_code,
    #             result_desc=result_desc,
    #             amount=amount,
    #             mpesa_receipt_number=mpesa_receipt_number,
    #             transaction_date=transaction_date,
    #             phone_number=phone_number
    #         )

    #         return JsonResponse({"message": "Callback received and saved"}, status=200)

    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)

    # return JsonResponse({"error": "Invalid request method"}, status=400)

# subscription
