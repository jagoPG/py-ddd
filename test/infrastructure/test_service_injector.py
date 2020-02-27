from unittest import TestCase

from app.infrastructure.service_injector import ServiceInjector, ServiceDoesNotExist, \
    ServiceAlreadyExists


class MockService:
    """
    A service mock for testing
    """


class ServiceInjectorTest(TestCase):
    def setUp(self):
        self.test_injector = ServiceInjector('test', '1.0')

    def test_service_can_be_created(self):
        mock_service = MockService()
        self.test_injector.service_consumer.register_service(
            'test_service_can_be_created', mock_service
        )
        assert 'test_service_can_be_created' in self.test_injector.service_consumer.services

    def test_service_does_not_exist(self):
        with self.assertRaises(ServiceDoesNotExist):
            self.test_injector.get_service('an_non_existing_service')

    def test_service_already_exists(self):
        with self.assertRaises(ServiceAlreadyExists):
            mock_service = MockService()
            another_service = MockService()
            self.test_injector.service_consumer.register_service(
                'test_service_can_be_created', mock_service
            )
            self.test_injector.service_consumer.register_service(
                'test_service_can_be_created', another_service
            )
