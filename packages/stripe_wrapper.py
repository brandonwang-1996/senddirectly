from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

#in reality this should be in an environmental variable
stripe.api_key = "sk_test_51PMywIKgoTqYhpheyE1LXrqdykuFYHeg1sNljVZnC89ZQ9vj9h71KvzcQa49si9gs3GaPRFUbf7uvoNx2p1GhmqG00jLbirhXq"

"""
Creates a connected account for the main Strip account to pay out
:param:
:return account: account id
:return account_link_url: onboarding url for recipient to verify through
"""

@app.route('/create_connected_account', methods=['POST'])
def create_connected_account():
    try:
        account = stripe.Account.create(
            type='express',
            country='US',
            email=request.json['email'],
        )
        
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url='localhost:5000/reauth',
            return_url='localhost:5000/return',
            type='account_onboarding',
        )

        return jsonify({
            'account': account,
            'account_link_url': account_link.url
        }), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/reauth')
def reauth():
    # Handle the case where the user needs to restart the onboarding process
    return "Please refresh and start the onboarding process again."

@app.route('/return')
def return_url():
    # Handle the case where the user returns after completing the onboarding process
    return "Thank you for completing the onboarding process!"

if __name__ == '__main__':
    app.run(debug=True)


"""
Sends a given amount of money to a given connected account
:param amount: amount to send out
:param connected_account_id: account id to send out to. Should be saved from create_connected_account
:return:
"""

def create_transfer(amount, connected_account_id):
    try:
        transfer = stripe.Transfer.create(
            amount=amount,
            currency='usd',
            destination=connected_account_id,
        )
        return jsonify(transfer), 200
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)


def extract_from_stripe_response():
    pass