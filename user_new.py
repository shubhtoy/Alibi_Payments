from re import M
import razorpay
from razorpay.errors import BadRequestError
from test_db import Payments

# name,phone,email,member_list,team name,return unique id in database.
client = razorpay.Client(auth=("rzp_test_vl1fGhuO2FWXvd", "uio0dtdi7tPrcSDxMp6ZCP5F"))


test_dict = {
    "team_name": "test12",
    "member_list": [
        {"name": "member1", "phone": "1234567890", "email": "member1@example.com"},
        {"name": "member2", "phone": "1234567890", "email": "member2@example.com"},
        {"name": "member3", "phone": "1234567890", "email": "member3@example.com"},
    ],
}


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
    "reference_id": None,
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
response_json = {
    "accept_partial": False,
    "amount": 300,
    "amount_paid": 0,
    "callback_method": "get",
    "callback_url": "https://shubhtoy.github.io/alibi_",
    "cancelled_at": 0,
    "created_at": 1659012218,
    "currency": "INR",
    "customer": {
        "contact": "+919520237711",
        "email": "shubhmittal.sm@gmail.com",
        "name": "Dhruv Mittal",
    },
    "description": "Rigistration of TEAM NAME",
    "expire_by": 0,
    "expired_at": 0,
    "first_min_partial_amount": 0,
    "id": "plink_Jyn3eOAeY4m2Ks",
    "notes": None,
    "notify": {"email": True, "sms": True},
    "payments": None,
    "reference_id": "#213ded",
    "reminder_enable": True,
    "reminders": [],
    "short_url": "https://rzp.io/i/ftaJRS8Y",
    "status": "created",
    "updated_at": 1659012218,
    "upi_link": False,
    "user_id": "",
}


def crud(action, data=None):
    # database entry

    database = Payments("PaymentDetails_test", "Alibi_Payment")
    # database.get_all_teams()
    if action == "create":
        database.create_team(data)
        print("created")
    elif action == "read":
        print("read")
    elif action == "read_teams":
        teams = database.get_all_teams()
        teams = [i["team_name"] for i in teams]
        # print(teams)
        # return print(list(database.get_all_teams()))
        return teams
    elif action == "update":
        team_name = data["team_name"]
        del data["team_name"]
        database.update_team(team_name, data)
        print("updated")
    else:
        print("error")
    return data


def send_link(registration_data):

    try:
        payment_json["amount"] = registration_data["payment_amount"]
        payment_json["customer"]["name"] = registration_data["primary_name"]
        payment_json["customer"]["email"] = registration_data["primary_email"]
        payment_json["customer"]["contact"] = registration_data["primary_phone"]
        payment_json["reference_id"] = registration_data["reference_id"]
        req = client.payment_link.create(payment_json)
        registration_data["payment_link"] = req["short_url"]
        registration_data["payment_id"] = req["id"]
        # registration_data["payment_pending"] = False
        del req["id"], req["short_url"]
        crud(data=registration_data, action="update")
        registration_data.update(req)
        print(registration_data)
        # print(req)
        return registration_data

    except Exception as e:
        print(e)
        a = client.payment_link.fetch(reference_id="2133")
        print(a)
        print("Already Generated")


def new_registration(user_data_dict):
    team_name = user_data_dict["team_name"]
    team_name_list = crud("read_teams")
    if team_name in team_name_list:
        return "Team name already exists"

    members = user_data_dict.get("member_list")
    member_data = {}
    for no, member in enumerate(members):
        no += 1
        # for details in member:
        member_data[f"member{no}_name"] = member["name"]
        member_data[f"member{no}_phone"] = member["phone"]
        member_data[f"member{no}_email"] = member["email"]
    registration_data = {
        "team_name": team_name,
        "reference_id": f"#{team_name}",
        "amount": 500,
        "count_members": len(members),
        "members": member_data,
        "payment_pending": True,
        "payment_amount": 50000,
        "payment_link": None,
        "payment_id": None,
        "primary_email": member_data["member1_email"],
        "primary_phone": member_data["member1_phone"],
        "primary_name": member_data["member1_name"],
    }
    # database entry
    crud(data=registration_data, action="create")

    return send_link(registration_data)


def get_registration_data(reference_id):
    registration_data = crud(data=reference_id, action="read")
    return registration_data


def get_team_names():
    return crud(action="read_teams")


def payment_complete(response_json):
    reference_id = response_json["payload"]["order"]["entity"]["receipt"][1:]
    payment_details = response_json["payload"]["payment"]
    registration_data = {}
    # registration_data = crud(data=reference_id, action="update")
    registration_data["payment_pending"] = False
    registration_data["team_name"] = reference_id
    registration_data["payment_details"] = payment_details
    print(registration_data)
    crud(data=registration_data, action="update")
    return registration_data


def parse_data(response_form):

    response_form = response_form["form_response"]["answers"]

    new_list = []
    # print(response_form)
    for i in response_form:
        print(i)
        try:
            new_list.append(i["text"])
        except:
            try:
                new_list.append(i["phone_number"])
            except:
                try:
                    new_list.append(i["email"])
                except:
                    new_list.append(i["choice"]["label"])

    if len(new_list) == 12:
        registration_data = {
            "team_name": new_list[0],
            "member_list": [
                {"name": new_list[2], "phone": new_list[3], "email": new_list[4]},
                {"name": new_list[6], "phone": new_list[7], "email": new_list[8]},
                {"name": new_list[9], "phone": new_list[10], "email": new_list[11]},
            ],
        }
    else:
        registration_data = {
            "team_name": new_list[0],
            "member_list": [
                {"name": new_list[2], "phone": new_list[3], "email": new_list[4]},
                {"name": new_list[6], "phone": new_list[7], "email": new_list[8]},
            ],
        }
    return registration_data
    # print(registration_data)


from flask import Flask, request, json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Webhooks with Python"


@app.route("/form/", methods=["POST", "GET"])
def new_form_filled():
    if request.method == "POST":
        data = request.json
        new_registration(parse_data(data))
        return "OK"
    elif request.method == "GET":
        return "FORM SERVER UP"


@app.route("/payments/", methods=["POST", "GET"])
def new_payment_made():
    if request.method == "POST":
        data = request.json
        # print(data)
        payment_complete(data)
        return "OK"
    elif request.method == "GET":
        return "PAYMENT SERVER UP"


if __name__ == "__main__":
    app.run(debug=True)
