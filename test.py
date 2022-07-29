import razorpay

client = razorpay.Client(auth=("rzp_test_vl1fGhuO2FWXvd", "uio0dtdi7tPrcSDxMp6ZCP5F"))
from razorpay.errors import BadRequestError

try:
    a = client.payment_link.create(
        {
            "amount": 300,
            "currency": "INR",
            "accept_partial": False,
            #   "first_min_partial_amount": 100,
            "description": "Rigistration of TEAM NAME",
            "customer": {
                "name": "Dhruv Mittal",
                "email": "shubhmittal.sm@gmail.com",
                "contact": "+919520237711",
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True,
            "reference_id": "#213ded",
            # "payment_link_id": "33",
            # "notes": {
            #     "policy_name": "Full Event Subscription",
            #     #    "policy_name": "Full Event Subscription"
            #     "ID": "1223444",
            # },
            "callback_url": "https://shubhtoy.github.io/alibi_",
            "callback_method": "get",
            "options": {
                "checkout": {"name": "ALIBI INC."},
                "hosted_page": {
                    "label": {
                        "receipt": "REF NO.",
                        "description": "TEAM NAME",
                        "amount_payable": "TEAM REGISTRATION FEES",
                    }
                },
            },
        }
    )
    print(a)


except BadRequestError:
    a = client.payment_link.fetch(reference_id="2133")
    print(a)
    print("Already Generated")


payment_json = {
    "amount": None,
    "description": "Registration to ALIBI INC.",
    "customer": {
        "name": None,
        "email": None,
        "contact": None,
    },
    "notify": {"sms": True, "email": True},
    "reminder_enable": True,
    "reference_id": "#223",
    "callback_url": "https://shubhtoy.github.io/alibi_",
    "callback_method": "get",
    "options": {
        "checkout": {"name": "ALIBI INC."},
        "hosted_page": {
            "label": {
                "receipt": "REF NO.",
                "description": "TEAM NAME",
                "amount_payable": "TEAM REGISTRATION FEES",
            }
        },
    },
}
