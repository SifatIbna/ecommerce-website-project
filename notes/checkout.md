# Checkout Process

1. Cart --> Checkout View
    ?
    - Login or Enter an Email (as Guest)
    - Shipping Address
    - Billing Info
        - Billing Address
        - Credit Card / Payment

2. Billing App/ Component
    - Billing Profile
        - User or Email (Guest Email)
        - generate payment processor token (Stripe or Braintee)

3. Orders / Invoices Component
    - Connecting the Billing Profile
    - Shipping / Billing Address
    - Cart
    - Status -- Shipped ? Cancelled? 
