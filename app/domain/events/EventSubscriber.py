import logging
from domain.model.Event import EventCreated
from infrastructure.domain_events import DomainEventSubscriber


class EventWasPublishedSubscriber(DomainEventSubscriber):
    def handle(self, domain_event) -> None:
        logging.info(
            'Heard that the event "{0}" was created at'.format(
                domain_event.name.name,
                domain_event.occurred_on.strftime('%Y-%m-%d %I:%M %S %p')
        ))

    def is_subscribed_to(self, domain_event) -> bool:
        return isinstance(domain_event, EventCreated)
