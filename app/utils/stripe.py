import stripe

# Set your Stripe API key
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


# Create a PaymentIntent
intent = stripe.PaymentIntent.create(
    amount=1000,  # amount in cents (e.g., $10.00)
    currency='usd',
)
