from unittest import TestCase

from app.infrastructure.service_injector import ServiceInjector, ServiceDoesNotExist, \
    ServiceAlreadyExists, YamlServiceFileParser, ServiceDefinition, ServiceRecorder, \
    FileCannotBeParsed


class FixtureService:
    """
    A service for testing
    """
    def __init__(self, fixture_service):
        self.fixture_service = fixture_service


class AnotherFixtureService:
    """
    A service for testing
    """


class ServiceInjectorTest(TestCase):
    """
    Tests that the service injector can store services, and does not allow
    to override existing services
    """

    def setUp(self):
        self.test_injector = ServiceInjector('test', '1.0')

    def test_service_can_be_created(self):
        mock_service = AnotherFixtureService()
        self.test_injector.service_consumer.register_service(
            'test_service_can_be_created', mock_service
        )
        assert 'test_service_can_be_created' in self.test_injector.service_consumer.services

    def test_service_does_not_exist(self):
        with self.assertRaises(ServiceDoesNotExist):
            self.test_injector.get_service('an_non_existing_service')

    def test_service_already_exists(self):
        with self.assertRaises(ServiceAlreadyExists):
            service = AnotherFixtureService()
            another_service = AnotherFixtureService()
            self.test_injector.service_consumer.register_service(
                'test_service_can_be_created', service
            )
            self.test_injector.service_consumer.register_service(
                'test_service_can_be_created', another_service
            )


class ServiceRecorderTest(TestCase):
    """
    Test that the service recorder adds the services properly to the
    service injector
    """

    def setUp(self) -> None:
        file_parser = YamlServiceFileParser()
        self.service_injector = ServiceInjector('test', '1.0')
        self.service_recorder = ServiceRecorder(
            self.service_injector, file_parser
        )

    def test_services_are_registered(self):
        self.service_recorder.record('test/resources/service_injector_fixture.yaml')
        self.assertEqual(2, len(self.service_injector.service_consumer.services))
        self.assertTrue(
            self.service_injector.is_service('test.service_injector.fixture_service')
        )
        self.assertTrue(
            self.service_injector.is_service('test.service_injector.another_fixture_service')
        )

    def test_service_file_is_incompatible(self):
        with self.assertRaises(FileCannotBeParsed):
            self.service_recorder.record('test/resources/service_injector_invalid_fixture.txt')


class YamlServiceFileParserTest(TestCase):
    """
    Tests that the file parser only processes YAML files properly
    """

    def setUp(self) -> None:
        self.file_parser = YamlServiceFileParser()

    def test_invalid_file_cannot_be_parsed(self) -> None:
        self.file_parser.set_filepath('test/resources/service_injector_invalid_fixture.txt')
        self.assertFalse(self.file_parser.can_be_parsed())

    def test_yaml_file_can_be_parsed(self) -> None:
        self.file_parser.set_filepath('test/resources/service_injector_fixture.yaml')
        self.assertTrue(self.file_parser.can_be_parsed())

    def test_fixture_file_shape_is_valid(self) -> None:
        expected_service_a = ServiceDefinition(
            'test.service_injector.fixture_service',
            'infrastructure.test_service_injector.AnotherFixtureService'
        )
        expected_service_a.add_dependency('test.service_injector.another_fixture_service')
        expected_service_a.add_tag('name', 'testing')
        expected_service_b = ServiceDefinition(
            'test.service_injector.another_fixture_service',
            'infrastructure.test_service_injector.FixtureService'
        )
        self.file_parser.set_filepath('test/resources/service_injector_fixture.yaml')
        parsed_services = {}
        for service in self.file_parser.parse_line():
            parsed_services[service.identifier] = service
        self.is_service_definition_equal(
            expected_service_a, parsed_services[expected_service_a.identifier]
        )
        self.is_service_definition_equal(
            expected_service_b, parsed_services[expected_service_b.identifier]
        )
        self.assertEqual(len(parsed_services), 2)

    def is_service_definition_equal(self, expected_service, service):
        self.assertEqual(
            expected_service.identifier,
            service.identifier
        )
        self.assertEqual(
            expected_service.dependencies,
            service.dependencies
        )
        self.assertEqual(
            expected_service.tag,
            service.tag
        )
