from fastapi import APIRouter, HTTPException
from paypalrestsdk import Payment

from app.database.db import get_db, Appointment

paypal_router = APIRouter(prefix="/paypal")

# Set your PayPal client ID and secret
PAYPAL_CLIENT_ID = 'Aa-JQbb9Qbw6LfXKSrL_yzVR_kgYtgQ3gfC9DuLVlOqx7iarc2OnFW6_rteAYDkb3_UseiKQE2YnWnoQ'
PAYPAL_SECRET = 'EANn24FkTssv0ZuyJXAU799PepBmLwOH0utrs5RwXyix23FJh38UrJi5PEWvQxRBJy0imXphxofxD_xV'

# Configure the PayPal SDK
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET
})


@paypal_router.get("/initiate-payment/{identifier}")
async def initiate_paypal_payment(identifier: int):

    try:
        db = get_db()
        appointment = db.query(Appointment).filter_by(identifier=identifier).first()
        price = appointment.service.price
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": price,
                    "currency": "USD"
                },
                "description": "Your payment description."
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/paypal/execute-payment",
                "cancel_url": "http://localhost:8000/paypal/cancel-payment"
            }
        })

        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    return link.href
        else:
            raise HTTPException(detail="Failed to create PayPal payment", status_code=500)

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


@paypal_router.get("/execute-payment")
async def execute_paypal_payment(paymentId: str, PayerID: str):
    try:
        payment = Payment.find(paymentId)

        if payment.execute({"payer_id": PayerID}):
            return {"status": "success", "message": "Payment executed successfully"}
        else:
            raise HTTPException(detail="Failed to execute PayPal payment", status_code=500)

    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
