import requests
from django.shortcuts import render, redirect
from uuid import UUID
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from homepro import settings
from datetime import datetime
from .models import MpesaTransaction
from django.shortcuts import render, get_object_or_404
from users.models import Booking
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.db import transaction
from bids.models import Bid
import math
def payment_options(request):
    booking_id_str = request.session.get('payment_booking_id')
    bid_id_str = request.session.get('payment_bid_id')  
    if not booking_id_str:
        return redirect('booking_history')
        
    try:
        booking_id = UUID(booking_id_str)
    except ValueError:
        return redirect('booking_history')
    bid= get_object_or_404(Bid, id=bid_id_str)
    booking = get_object_or_404(Booking, id=booking_id, user=request.user.profile)
    return render(request, 'payments/payment_options.html', {
        'booking': booking,
        'bid': bid
    })
# process payments
def process_payment(request):
    if request.method == 'POST':
        
        booking_id = request.session.get('payment_booking_id')
        bid_id = request.session.get('payment_bid_id')
        
        if not booking_id:
            return redirect('booking_history')
            
        booking = get_object_or_404(Booking, id=booking_id, user=request.user.profile)
        bid = get_object_or_404(Bid, id=bid_id, booking__user=request.user.profile)
        
        payment_method = request.POST.get('payment_method')
        # Debugging
        # print(f"Payment method selected: {payment_method}") 
        # print(f"Booking ID: {booking_id}")
        user_phone = request.user.profile.phone
        bid_amount = math.ceil(bid.price)
        # print(f"User phone number: {user_phone}")
        try:
            with transaction.atomic():
                # Process payment (implement your payment gateway logic here)
                if payment_method == 'mpesa':
                    headers = {
                            'Authorization': 'Bearer FdOSb2bmVAqL3JpGi3yifkWusF3j'
                            }
                    payload = {
                        "BusinessShortCode": 174379,
                        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjUwNDExMDcwODEz",
                        "Timestamp": "20250411070813",
                        "TransactionType": "CustomerPayBillOnline",
                        "Amount": bid_amount,
                        "PartyA": 254707485760,
                        "PartyB": 174379,
                        "PhoneNumber": user_phone,
                        "CallBackURL": "https://mydomain.com/path",
                        "AccountReference": "HomePro",
                        "TransactionDesc": "Kushpedia" 
                            }
                    

                    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                headers = headers, json = payload)
                    try:
                        response_data = response.json() # Mpesa Response
                        
                        # print("Response from M-Pesa:", response_data)  # Debugging
                        
                        mpesa_request_code = response_data['ResponseDescription']
                        if mpesa_request_code =='Success. Request accepted for processing':                            
                            
                            booking.status = 'confirmed'
                            #Optionally: Reject all other bids for this booking
                            
                            
                            booking.booking_bid_s.exclude(id=bid_id).update(status='rejected')
                            
                            bid.status = 'accepted'
                            bid.accepted_at= datetime.now()
                            bid.save()
                            booking.save()
                            # Send notifications
                            send_bid_accepted_notification(bid)
                            messages.success(request,"Your Payment Was successful")
                            
                        else:
                            messages.error(request,"Your Payment failed try Again")
                    except ValueError:
                        response_data = {"error": "Your Payment failed try Again"}

                    
                    # payment_success = process_mpesa_payment(booking)
                elif payment_method == 'card':
                    print('Card triggered')
                    # payment_success = process_card_payment(booking)
                else:
                    print('Invalid payment method')
        except Exception as e:
            messages.error(request, f"Payment error: {str(e)}")
            return redirect('payment_options')
    
    return redirect('booking_history')

def send_bid_accepted_notification(bid):
    subject = f"Your bid for {bid.booking.service.name} has been accepted!"
    message = f"""
    🎉 Congratulations {bid.provider.first_name}!,
    
    Your bid of Ksh {bid.price:,.2f} for {bid.booking.service.name} has been accepted!
    
    📌 Service: {bid.booking.service.name}
    👤 Client: {bid.booking.user.first_name}
    📞 Contact: {bid.booking.user.phone}
    📅 Date: {bid.booking.date.strftime('%A, %B %d, %Y at %I:%M %p')}
    📍 Location: {bid.booking.user.location}
    📝 Notes: {bid.booking.special_instructions or 'None'}
    
    Please contact the client within 3 hours to confirm details. 🤝
    
    Thank you for using our platform! 💙
    """
    
    email = EmailMessage(
        subject=subject,
        body=message.strip(),
        from_email=settings.EMAIL_HOST_USER,
        to=[bid.provider.email],
    )

    
    email.cc = [bid.booking.user.email]

    email.send(fail_silently=False)

@csrf_exempt
def mpesa_callback(request):
    pass
    