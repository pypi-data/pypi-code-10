from __future__ import absolute_import

# import models into sdk package
from .models.patch_account_request import PatchAccountRequest
from .models.create_charge_request import CreateChargeRequest
from .models.get_banknote_response import GetBanknoteResponse
from .models.get_payment_response import GetPaymentResponse
from .models.create_charge_response import CreateChargeResponse
from .models.get_charge_response import GetChargeResponse
from .models.create_token_response import CreateTokenResponse
from .models.create_payment_response import CreatePaymentResponse
from .models.get_payments_response_payment import GetPaymentsResponsePayment
from .models.get_tokens_response_token_terms import GetTokensResponseTokenTerms
from .models.redeem_banknote_response import RedeemBanknoteResponse
from .models.currency_code import CurrencyCode
from .models.get_account_response import GetAccountResponse
from .models.get_accounts_response import GetAccountsResponse
from .models.money import Money
from .models.get_tokens_response import GetTokensResponse
from .models.get_token_response import GetTokenResponse
from .models.create_token_request_terms import CreateTokenRequestTerms
from .models.patch_token_request_terms import PatchTokenRequestTerms
from .models.redeem_banknote_request import RedeemBanknoteRequest
from .models.get_banknotes_response_banknote import GetBanknotesResponseBanknote
from .models.get_receipt_response import GetReceiptResponse
from .models.get_token_response_terms import GetTokenResponseTerms
from .models.create_account_response import CreateAccountResponse
from .models.get_balance_response import GetBalanceResponse
from .models.create_payment_request import CreatePaymentRequest
from .models.patch_token_request import PatchTokenRequest
from .models.create_receipt_request import CreateReceiptRequest
from .models.get_charges_response import GetChargesResponse
from .models.math_context import MathContext
from .models.get_receipts_response_receipt import GetReceiptsResponseReceipt
from .models.get_banknotes_response import GetBanknotesResponse
from .models.create_token_request import CreateTokenRequest
from .models.create_account_request import CreateAccountRequest
from .models.get_payments_response import GetPaymentsResponse
from .models.get_charges_response_charge import GetChargesResponseCharge
from .models.get_charge_response_terms import GetChargeResponseTerms
from .models.create_receipt_response import CreateReceiptResponse
from .models.big_int import BigInt
from .models.get_receipts_response import GetReceiptsResponse
from .models.big_integer import BigInteger
from .models.get_accounts_response_account import GetAccountsResponseAccount
from .models.get_tokens_response_token import GetTokensResponseToken
from .models.get_charges_response_charge_terms import GetChargesResponseChargeTerms

# Identity service models
from .models.get_banks_response import GetBanksResponse
from .models.get_member_response import GetMemberResponse
from .models.create_device_response import CreateDeviceResponse
from .models.link_bank_request import LinkBankRequest
from .models.patch_member_request import PatchMemberRequest
from .models.finite_duration import FiniteDuration
from .models.create_member_request_device import CreateMemberRequestDevice
from .models.patch_device_request import PatchDeviceRequest
from .models.get_banks_response_bank import GetBanksResponseBank
from .models.create_member_request import CreateMemberRequest
from .models.create_device_request import CreateDeviceRequest
from .models.get_devices_response_device import GetDevicesResponseDevice
from .models.create_member_response import CreateMemberResponse
from .models.get_devices_response import GetDevicesResponse

# Settlement service models
from .models.system_check_response import SystemCheckResponse
from .models.currency_unit import CurrencyUnit
from .models.get_transfer_response import GetTransferResponse
from .models.create_settlement_request import CreateSettlementRequest
from .models.create_settlement_response_entry import CreateSettlementResponseEntry
from .models.create_settlement_response_transfer import CreateSettlementResponseTransfer
from .models.get_transfers_response import GetTransfersResponse
from .models.system_state_response_property import SystemStateResponseProperty
from .models.math_context import MathContext
from .models.create_transfer_request import CreateTransferRequest
from .models.money import Money
from .models.system_state_response import SystemStateResponse
from .models.create_transfer_response import CreateTransferResponse
from .models.create_settlement_response import CreateSettlementResponse
from .models.get_transfers_response_transfer import GetTransfersResponseTransfer

# src
from .apis.combined_banknote_api import BankNoteService as BNS
from .apis.combined_identity_api import IdentityService as IS
from .apis.combined_settlement_api import SettlementService as SS
from .src.Crypto import generate_keys

import os
script_path = os.path.dirname(os.path.abspath( __file__ ))

accounts = {"b846":{
                "clientId":"8c483e42-80d8-4377-9f61-d0d96b6e6a73",
                "bankAccountId":"b8466967-4aed-4661-9703-8ab43bb6ac60"},
            "f4ae":{
                "clientId":"6f183efd-12ab-430f-909a-51f9a3adfd8d",
                "bankAccountId":"f4ae5e44-0c80-4dcd-a2ac-b78c13ea055c"},
            "dec7": {
                "clientId":"6dfd7aa9-9ec6-4c4e-a706-089da23e916c",
                "bankAccountId":"dec7e2eb-9ecc-4a4b-9dbe-eebd1a1a92c7"},
            "b55f": {
                "clientId": "0f42abae-2e2f-4ceb-a8e1-800aff6d148b",
                "bankAccountId": "b55fb082-cb57-424c-8b28-e809a3d3438a"},
            "a63a":{
                "clientId":"9e997f7d-9758-405e-a347-f6243e2c622b",
                "bankAccountId": "a63a87ff-5515-4def-8eb9-19acdb673752"},
            "bc91":{
                 "clientId": "b6b53f0d-8729-4646-a4d3-767a5e5b3030",
                 "bankAccountId": "bc91e27a-4e5b-4d3f-acb9-6ef12bb408a3"},
            "c337":{
                  "clientId": "5b5af11f-795a-4bd5-b9b1-70a84092a189",
                  "bankAccountId": "c3377f82-5b87-4929-9676-ca5d0bb95f21"},
            "f944":{
                  "clientId": "5b5af11f-795a-4bd5-b9b1-70a84092a189",
                  "bankAccountId": "f94461d0-9f4c-4266-971b-31346f6ba603"}
            }
context = None
debug = False

def demo(demo_num):
    try:
        f = open(os.path.join(script_path,'src/demo/demo' + str(demo_num) + '.py'))
        print(f.read())
    except IOError:
        print("Demo does not exist.")

def welcome_message():
    print("Welcome to the Token console. Type Token.help() for help.")

def help():
    print("+-------------------------------------------------------------+")
    print("| Welcome to the Token console. Here we can issue commands to |")
    print("| interact with the Token system.                             |")
    print("+-------------------------------------------------------------+")
    print("| ACCOUNTS                                                    |")
    print("| bofa checking account: 'f4ae'                               |")
    print("| bofa savings account: 'dec7'                                |")
    print("| citi AMCE merchant account: 'a63a'                          |")
    print("| wells checking account: 'c337'                              |")
    print("| wells savings account: 'f944'                               |")
    print("+-------------------------------------------------------------+")
    print("| COMMANDS - Token                                            |")
    print("| Token.BankNoteService(bank_code)   // citi or bofa          |")
    print("| Token.IdentityService()                                     |")
    print("| Token.generate_keys()                                       |")
    print("| Token.switchContext(new_context)   // citi, alice, token,et |")
    print("| Token.demo(2)                       // show demo (1-3)      |")
    print("| Token.help()                       // print this            |")
    print("|                                                             |")
    print("| COMMANDS - Identity Service                                 |")
    print("| IS.create_member(keys)                                      |")
    print("| IS.get_member(keys)                                         |")
    print("|                                                             |")
    print("| COMMANDS - Banknote Service                                 |")
    print("| bofa.create_account(member, '6dfd')   // provide acc code   |")
    print("| bofa.get_balance(account)                                   |")
    print("| bofa.create_token(account, payee, amount, curr [, maxCount])|")
    print("| bofa.redeem_token(token, amount, curr)  // gets banknote    |")
    print("| bofa.deposit_banknote(account, banknote)                    |")
    print("|                                                             |")
    print("| COMMANDS - SettlementService                                |")
    print("| SS.settle()                       // trigger a settle       |")
    print("+-------------------------------------------------------------+")
    print("| You can use dir(object) to see what methods its has.        |")
    print("+-------------------------------------------------------------+")


def switchContext(c):
    global context
    context = c

class BankNoteService(BNS):
    def __init__(self, api_client=None):
        super(BankNoteService, self).__init__(api_client)

    def get_accounts(self, member_id):
        return super(BankNoteService, self).get_accounts(member_id)

    def get_balance(self, acc):
        if context != 'alice' and context != 'bob' and context != 'carol':
            print("Error: need member context.")
            return None
        accountId = acc.id
        return super(BankNoteService, self).get_balance(accountId)

    def create_token(self, acc, payee, amount, currency, maxCount= 100, request=None):
        if context != 'alice' and context != 'bob' and context != 'carol':
            print("Error: need member context.")
            return None
        if request is None:
            request ={
              "payeeMemberId": payee.member_id,
              "description": "demo",
              "terms": {
                "maxAmount": {
                  "value": str(amount),
                  "unit": currency
                },
                "maxCount": maxCount
              }
            }
        ret =super(BankNoteService, self).create_token(acc.id, request)
        if debug: print(ret)
        return ret

    def redeem_token(self, token, amount, currency, request=None):
        if context != 'alice' and context != 'bob' and context != 'carol':
            print("Error: need member context.")
            return None
        if request is None:
            request ={
                "amount": {
                  "value": str(amount),
                  "unit": currency
                },
                "description": ""
            }
        ret = super(BankNoteService, self).create_charge(token.id, request)
        if debug: print(ret)
        print(ret)
        banknote = {'id':ret.id, 'banknote_id': ret.banknote_id, 'bank_code':self.bank_code}
        return banknote


    def deposit_banknote(self, acc, banknote, request=None):
        if context != 'alice' and context != 'bob' and context != 'carol':
            print("Error: need member context.")
            return None
        if request is None:
            request ={
              "description": "bofa",
              "payerBankCode": banknote['bank_code'],
              "payerBanknoteId": banknote['banknote_id']
            }
        ret = super(BankNoteService, self).create_receipt(acc.id, request)
        if debug: print(ret)
        return ret

    def create_account(self, user, clientId, request=None):
        if context != 'citi' and context != 'bofa' and context!='wells':
            print("Error: need bank context.")
            return None
        if clientId[:4] not in accounts:
            print("Error: entered an invalid account.")
            return None
        accInfo = accounts[clientId[:4]]
        if request is None:
          request = {"bankAccountId": accInfo["bankAccountId"],
          "memberId": user.member_id,
          "memberPublicKey": user.keys[0],
          "memberPinPublicKey": "123",
          "name": "user"}
        ret = super(BankNoteService, self).create_account(accInfo["clientId"], request)
        if debug: print(ret)
        return ret


class IdentityService(IS):
    def __init__(self, api_client=None):
        super(IdentityService, self).__init__(api_client)

    def create_member(self, keys, request=None):
        if context != 'token':
            print('Error: need token context.')
            return None
        if request is None:
            if len(keys) < 2: return None
            request ={"name": "Anon","publicKey": keys[0],
                      "pinPublicKey": "123",
                      "device": {
                        "name": "dev1",
                        "pushNotificationId": "123",
                        "publicKey": "123"
                      }
                    }
        user = super(IdentityService, self).post_member(request)
        if user is not None:
            user.keys = keys
        if debug: print(user)
        return user

class SettlementService(SS):
    def __init__(self, api_client=None):
        super(SettlementService, self).__init__(api_client)

    def settle(self, request=None):
        if context != 'token':
            print('Error: need token context.')
            return None
        if request is None:
            request = {"description":"python"}
        ret = super(SettlementService, self).post_settlement(request)
        if debug: print(ret)
        return ret

# import ApiClient
from .api_client import ApiClient

from .configuration import Configuration

configuration = Configuration()
welcome_message()
