from datetime import datetime


class DomainEventPublisher:
    """
    Singleton class that holds the subscribers to the domain event bus, and notifies then
    when a domain event is published.
    """
    PUBLISHER_INSTANCE = None

    def __init__(self):
        self.subscribers = {}

    @staticmethod
    def get_instance() -> object:
        """
        Singleton

        :return: The instance of `DomainEventPublisher`
        """
        instance = DomainEventPublisher.PUBLISHER_INSTANCE
        if instance is not None:
            return instance
        instance = DomainEventPublisher.PUBLISHER_INSTANCE = DomainEventPublisher()
        return instance

    def subscribe(self, identifier, domain_event_subscriber) -> None:
        """
        Subscribes a DomainEventSubscriber to the Domain Event

        :param identifier: Identifier of the subscriber
        :param domain_event_subscriber: The domain event subscriber instance
        :raises SubscriberAlreadyExist, NotADomainEventSubscriber
        """
        if identifier in self.subscribers:
            raise SubscriberAlreadyExist
        if not isinstance(domain_event_subscriber, DomainEventSubscriber):
            raise NotADomainEventSubscriber
        self.subscribers[identifier] = domain_event_subscriber

    def unsubscribe(self, identifier) -> None:
        """
        Unsubscribes a DomainEventSubscriber from the Domain Event

        :param identifier: The identifier of the subscriber
        :raises SubscriberDoesNotExist:
        """
        if identifier not in self.subscribers:
            raise SubscriberDoesNotExist
        del self.subscribers[identifier]

    def publish(self, domain_event) -> None:
        """
        Notifies about a `domain_event` to all subscribers

        :param domain_event: DomainEventSubscriber
        """
        for item in self.subscribers.values():
            if item.is_subscribed_to(domain_event):
                item.handle(domain_event)


class DomainRoot:
    """
    The domain root class has to implement this to publish domain events.
    """

    def __init__(self):
        self.events = []
        self.domain_event_publisher = DomainEventPublisher.get_instance()

    def append(self, domain_event) -> None:
        """
        Store an event to be launched later

        :param domain_event:
        """
        self.events.append(domain_event)

    def release(self) -> None:
        """
        Launch all events that have been recorded
        """
        for event in self.events:
            self.domain_event_publisher.publish(event)
        self.clear()

    def clear(self) -> None:
        """
        Remove all recorded events
        """
        self.events.clear()


class DomainEvent:
    """
    Template for a domain event
    """

    def __init__(self):
        self._occurred_on = datetime.now()

    @property
    def occurred_on(self) -> datetime:
        """
        :return: When the domain event has been created
        """
        return self._occurred_on


class DomainEventSubscriber:
    """
    Template for a service subscribed to a domain event
    """

    def is_subscribed_to(self, domain_event) -> bool:
        """
        Validates the domain event this class is subscribed to

        :param domain_event: Instance implementing `DomainEvent`
        :return: bool
        """
        raise NotImplementedError

    def handle(self, domain_event) -> None:
        """
        Executes an action

        :param domain_event: event that triggers the action
        """
        raise NotImplementedError


class SubscriberAlreadyExist(Exception):
    """
    A subscriber has already been added to the Domain Event Bus
    """


class SubscriberDoesNotExist(Exception):
    """
    A subscriber does not exist in the Domain Event Bus
    """


class NotADomainEventSubscriber(Exception):
    """
    A subscriber does not implement DomainEventSubscriber contract
    """
