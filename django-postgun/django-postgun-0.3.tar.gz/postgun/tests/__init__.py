EVENTS_ERROR_URL = "https://api.mailgun.net/v3/example.com/events?end=Fri%2C+13+Nov+2015+15%3A11%3A49+UTC&begin=Fri%2C+13+Nov+2015+15%3A11%3A49+UTC&limit=1&ascending=True"
EVENTS_ERROR = u'{\n  "message": "Inconsistent range: begin=2015-11-13 15:11:49+00:00, end=2015-11-13 15:11:49+00:00, ascending=True"\n}'


EVENTS_PAGE_ONE_URL = 'https://api.mailgun.net/v3/example.com/events?begin=Fri%2C+06+Nov+2015+15%3A11%3A23+UTC&limit=1&ascending=True'
EVENTS_PAGE_TWO_URL = 'https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6Mjk6MDguNjI3KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsICJtZXNzYWdlI21DbmdrQkp3UWs2UUpWR3NpSjR1ZEEiXQ=='
EVENTS_PAGE_THREE_URL = 'https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6Mjk6MjQuNDYzKzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsICJtZXNzYWdlI2xpMlFLN3h4UXotU01fMHVydVZRbnciXQ=='

EVENTS_PAGE_ONE = """
{
  "items": [
    {
      "tags": [],
      "timestamp": 1447255748.627257,
      "envelope": {
        "targets": "james@example.com",
        "transport": "smtp",
        "sender": "hello@example.com"
      },
      "recipient-domain": "example.com",
      "method": "http",
      "campaigns": [],
      "user-variables": {},
      "flags": {
        "is-routed": null,
        "is-authenticated": true,
        "is-system-test": false,
        "is-test-mode": false
      },
      "log-level": "info",
      "id": "mCngkBJwQk6QJVGsiJ4udA",
      "message": {
        "headers": {
          "to": "james.vandyne@example.com",
          "message-id": "20151111152908.17071.97735@example.com",
          "from": "hello@example.com",
          "subject": "Good Morning James"
        },
        "attachments": [],
        "recipients": [
          "james.vandyne@example.com"
        ],
        "size": 346
      },
      "recipient": "james.vandyne@example.com",
      "event": "accepted"
    }
  ],
  "paging": {
    "next": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6Mjk6MDguNjI3KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsICJtZXNzYWdlI21DbmdrQkp3UWs2UUpWR3NpSjR1ZEEiXQ==",
    "last": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIHsiYiI6ICIyMDM3LTEyLTMxVDIzOjU5OjU5Ljk5OSswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgbnVsbF0=",
    "first": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsIG51bGxd",
    "previous": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjg0KzAwOjAwIn0sIHsiYiI6ICIyMDE1LTExLTExVDE1OjI5OjA4LjYyNyswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuMjgzKzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgIm1lc3NhZ2UjbUNuZ2tCSndRazZRSlZHc2lKNHVkQSJd"
  }
}
"""

EVENTS_PAGE_TWO = """
{
  "items": [
    {
      "tags": [],
      "delivery-status": {
        "tls": true,
        "mx-host": "example-smtp-in.l.example.com",
        "code": 0,
        "description": null,
        "session-seconds": 0.5392341613769531,
        "message": "",
        "certificate-verified": true
      },
      "envelope": {
        "transport": "smtp",
        "sender": "hello@example.com",
        "sending-ip": "209.61.151.224",
        "targets": "james.vandyne@example.com"
      },
      "recipient-domain": "example.com",
      "id": "li2QK7xxQz-SM_0uruVQnw",
      "campaigns": [],
      "user-variables": {},
      "flags": {
        "is-routed": null,
        "is-authenticated": true,
        "is-system-test": false,
        "is-test-mode": false
      },
      "log-level": "info",
      "timestamp": 1447255764.463081,
      "message": {
        "headers": {
          "to": "james.vandyne@example.com",
          "message-id": "20151111152908.17071.97735@example.com",
          "from": "hello@example.com",
          "subject": "Good Morning James"
        },
        "attachments": [],
        "recipients": [
          "james.vandyne@example.com"
        ],
        "size": 492
      },
      "recipient": "james.vandyne@example.com",
      "event": "delivered"
    }
  ],
  "paging": {
    "next": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6Mjk6MjQuNDYzKzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsICJtZXNzYWdlI2xpMlFLN3h4UXotU01fMHVydVZRbnciXQ==",
    "last": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIHsiYiI6ICIyMDM3LTEyLTMxVDIzOjU5OjU5Ljk5OSswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgbnVsbF0=",
    "first": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsIG51bGxd",
    "previous": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA4KzAwOjAwIn0sIHsiYiI6ICIyMDE1LTExLTExVDE1OjI5OjI0LjQ2MyswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjcuNzA3KzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgIm1lc3NhZ2UjbGkyUUs3eHhRei1TTV8wdXJ1VlFudyJd"
  }
}
"""

EVENTS_PAGE_THREE = """
{
  "items": [
  ],
  "paging": {
    "next": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MzA6MTUuNzQ0KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsICJtZXNzYWdlI0N6d2MxcTFpUjhHY2dKNUx0YWFOTkEiXQ==",
    "last": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIHsiYiI6ICIyMDM3LTEyLTMxVDIzOjU5OjU5Ljk5OSswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgbnVsbF0=",
    "first": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIHsiYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIFsiZiJdLCBudWxsLCBbWyJhY2NvdW50LmlkIiwgIjU1YzI1YTJkMDQ1Y2E0NjE5NGJiMjg3ZCJdLCBbImRvbWFpbi5uYW1lIiwgImt3b29zaC5jb20iXV0sIDEsIG51bGxd",
    "previous": "https://api.mailgun.net/v3/example.com/events/W3siYSI6IHRydWUsICJiIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA4KzAwOjAwIn0sIHsiYiI6ICIyMDE1LTExLTExVDE1OjMwOjE1Ljc0NCswMDowMCIsICJlIjogIjIwMTUtMTEtMTFUMTU6MTc6MjguMTA3KzAwOjAwIn0sIFsicCIsICJmIl0sIG51bGwsIFtbImFjY291bnQuaWQiLCAiNTVjMjVhMmQwNDVjYTQ2MTk0YmIyODdkIl0sIFsiZG9tYWluLm5hbWUiLCAia3dvb3NoLmNvbSJdXSwgMSwgIm1lc3NhZ2UjQ3p3YzFxMWlSOEdjZ0o1THRhYU5OQSJd"
  }
}
"""
