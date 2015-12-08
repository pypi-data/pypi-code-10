from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry

class EventBuilder(ArchetypesBuilder):
    portal_type = 'Event'


builder_registry.register('event', EventBuilder)