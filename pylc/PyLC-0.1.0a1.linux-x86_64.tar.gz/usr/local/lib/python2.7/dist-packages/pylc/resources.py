# The MIT License (MIT)
# 
# Copyright (c) 2015 Benjamin Morrise
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from utils import build_data

class AccountResource:

  resource = 'accounts'

  def __init__(self, lc):
    self.lc = lc

  def summary(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'summary'))

  def available_cash(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'availablecash'))

  def transfer_funds(self, amount, transfer_frequency, start_date=None, end_date=None):
    data = build_data({
      "transferFrequency": transfer_frequency,
      "amount": amount,
      "startDate": start_date,
      "endDate": end_date,
      })
    return self.lc._call((self.resource, self.lc.investor_id, 'funds', 'add'), data=data)

  def pending_transfers(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'funds', 'pending'))

  def cancel_transfers(self, transfer_ids):
    data = build_data({
      "transferIds": transfer_ids
      })
    return self.lc._call((self.resource, self.lc.investor_id, 'funds', 'cancel'), data=data)    

  def notes_owned(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'notes'))

  def detailed_notes_owned(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'detailednotes'))

  def portfolios_owned(self):
    return self.lc._call((self.resource, self.lc.investor_id, 'portfolios'))

  def create_portfolio(self, portfolio_name, portfolio_description):
    data = build_data({
      "investorId": self.lc.investor_id,
      "portfolioName": portfolio_name,
      "portfolioDescription": portfolio_description
      })
    return self.lc._call((self.resource, self.lc.investor_id, 'portfolios'), data=data)

class LoanResource:

  resource = 'loans'

  def __init__(self, lc):
    self.lc = lc

  def listing(self, as_of_date=None, show_all=False):
    query_string = build_data({
      "AsOfDate": as_of_date,
      "showAll": show_all
      })
    return self.lc._call((self.resource, 'listing'), query_string=query_string)    
