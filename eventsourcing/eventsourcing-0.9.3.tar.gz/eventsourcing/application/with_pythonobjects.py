from eventsourcing.application.base import EventSourcingApplication
from eventsourcing.infrastructure.stored_events.base import InMemoryStoredEventRepository


class EventSourcingWithPythonObjects(EventSourcingApplication):

    def create_stored_event_repo(self):
        return InMemoryStoredEventRepository()
