from unittest import TestCase
from unittest.mock import MagicMock
from app.infrastructure.domain_events import DomainEventPublisher, DomainEvent, DomainRoot, \
    DomainEventSubscriber, SubscriberDoesNotExist, SubscriberAlreadyExist


class DomainEventsTest(TestCase):
    def setUp(self):
        self.domainEventPublisher = DomainEventPublisher()
        self.domainEventPublisher.subscribers = {}

    def test_event_subscriber_is_registered(self):
        subscriber = ProductHasBeenPublishedSubscriber()
        self.domainEventPublisher.subscribe('product_is_published_subscriber', subscriber)
        self.assertIsNotNone(
            self.domainEventPublisher.subscribers['product_is_published_subscriber']
        )

    def test_event_subscriber_is_not_registered(self):
        with self.assertRaises(SubscriberDoesNotExist):
            self.domainEventPublisher.unsubscribe('an_non_registered_event')

    def test_event_subscriber_is_already_registered(self):
        subscriber = ProductHasBeenPublishedSubscriber()
        self.domainEventPublisher.subscribe('product_is_published_subscriber', subscriber)
        with self.assertRaises(SubscriberAlreadyExist):
            another_subscriber = ProductHasBeenPublishedSubscriber()
            self.domainEventPublisher.subscribe(
                'product_is_published_subscriber', another_subscriber
            )

    def test_event_is_published(self):
        event = ProductHasBeenPublished('Helix')
        subscriber = ProductHasBeenPublishedSubscriber()
        subscriber.handle = MagicMock()
        self.domainEventPublisher.subscribe('product_is_published_subscriber', subscriber)
        self.domainEventPublisher.publish(event)
        subscriber.handle.assert_called_with(event)

    def test_event_is_not_published(self):
        event = EventWithoutSubscribers()
        subscriber = ProductHasBeenPublishedSubscriber()
        subscriber.handle = MagicMock()
        subscriber.is_subscribed_to = MagicMock(return_value=False)
        self.domainEventPublisher.subscribe('product_is_published_subscriber', subscriber)
        self.domainEventPublisher.publish(event)
        subscriber.is_subscribed_to.assert_called_with(event)
        subscriber.handle.assert_not_called()

    def test_domain_root_caches_events(self):
        expected_name = 'Helix'
        product = Product('Helix')
        product.published()
        stored_events = product.events
        self.assertTrue(len(stored_events) == 1)
        self.assertTrue(isinstance(stored_events[0], ProductHasBeenPublished))
        self.assertTrue(stored_events[0].name, expected_name)

    def test_domain_root_publishes_events(self):
        self.domainEventPublisher.publish = MagicMock()
        product = Product('Helix')

        # Keep in the test and the DomainRoot the same instance of the DomainEventPublisher. As
        # it is a singleton, a normal use in the test will refer to a different instance.
        product.domain_event_publisher = self.domainEventPublisher

        product.published()
        expected_event = product.events[0]
        product.release()
        self.assertTrue(len(product.events) == 0)
        self.domainEventPublisher.publish.assert_called_with(expected_event)

    def test_domain_root_events_are_cleared(self):
        product = Product('Helix')
        product.published()
        product.clear()
        self.assertTrue(len(product.events) == 0)


class Product(DomainRoot):
    def __init__(self, name):
        super(Product, self).__init__()
        self.name = name

    def published(self):
        self.append(
            ProductHasBeenPublished(self.name)
        )


class ProductHasBeenPublished(DomainEvent):
    def __init__(self, name):
        super(ProductHasBeenPublished, self).__init__()
        self.name = name


class EventWithoutSubscribers(DomainEvent):
    """
    For testing an event that is not registered and should not be
    triggered.
    """


class ProductHasBeenPublishedSubscriber(DomainEventSubscriber):
    def handle(self, domain_event):
        print('The product with name {0} has been published!'.format(domain_event.name))

    def is_subscribed_to(self, domain_event):
        return isinstance(domain_event, ProductHasBeenPublished)
