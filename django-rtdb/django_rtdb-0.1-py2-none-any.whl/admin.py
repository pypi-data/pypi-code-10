from django.contrib import admin

from .models import (
    Customfield,
    CustomfieldValue,
    Objectcustomfieldvalues,
    Queue,
    TicketCustomfieldValue,
    TicketCustomfieldValueManager,
    Ticket,
)

admin.site.register(Customfield)
admin.site.register(CustomfieldValue)
admin.site.register(Objectcustomfieldvalues)
admin.site.register(Queue)
admin.site.register(TicketCustomfieldValue)
admin.site.register(TicketCustomfieldValueManager)
admin.site.register(Ticket)
