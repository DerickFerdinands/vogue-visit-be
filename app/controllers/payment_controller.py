from fastapi import APIRouter, Depends, HTTPException

import stripe

payment_router = APIRouter(prefix="/payments")




@payment_router.get("/")
async def fetch_user():
    stripe.api_key = 'sk_test_51Oal73GrGmvycgSCellBFMNK0e3vnq7ql74XwRp4i463b7uHbwf52qODS7VWF5AK5vDEcM34dG0OabtCGk5Jsr8E00M3QcJzKV'

    try:
        # Create a PaymentIntent
        print(f"API Key set to: {stripe.api_key}")
        intent = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
        )

        # Redirect the user to the payment gateway using the client_secret
        return f"https://checkout.stripe.com/pay/{intent.client_secret}"
    except stripe.error.CardError as e:
        # Handle card errors
        raise HTTPException(detail=str(e.error.message), status_code=400)


@payment_router.get("/all")
async def fetch_user1():
    return "hello"
