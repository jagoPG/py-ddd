"""
The conversion from file definition to instance has been based on:
https://github.com/jagoPG/restaurant-ml-inspector
"""
from typing import Generator

from yaml import load, Loader


class ServiceInjector:
    """
    Provides access to registered services
    """

    def __init__(self, name, version):
        """
        :param name: Name of the service injector
        :param version: Version of the service injector
        """
        self.name = name
        self.version = version
        self.service_consumer = ServiceConsumer()

    def is_service(self, identifier) -> bool:
        """
        Checks if a service identifier is already registered
        :param identifier: The identifier of the service
        :return:
        """
        return identifier in self.service_consumer.services

    def get_service(self, identifier):
        """
        Gets a registered service

        :param identifier: The identifier of the registered service
        :return: The instance of the service
        """
        if identifier not in self.service_consumer.services:
            raise ServiceDoesNotExist
        return self.service_consumer.services[identifier]


class ServiceConsumer:
    """
    Stores the services of the service injector
    """

    def __init__(self):
        self.services = {}

    def register_service(self, identifier, service):
        """
        Registers a service in the ServiceInjector

        :param identifier: An unique identifier for the service
        :param service: An instance of the service
        :raises: ServiceAlreadyExists
        """
        if identifier in self.services:
            raise ServiceAlreadyExists
        self.services[identifier] = service


class ServiceRecorder:
    """
    Parses a definition file with all services, and registers in a `DependencyInjector`
    """

    def __init__(self, service_injector, parser):
        """
        :param service_injector: A `ServiceInjector` to store the instances
        :param parser: A `ServiceFileParser` to read the definition file
        """
        self.service_injector = service_injector
        self.parser = parser

    def record(self, file_location) -> None:
        """
        :param file_location: Location of the service definition file
        """
        self.parser.set_filepath(file_location)
        if not self.parser.can_be_parsed():
            raise FileCannotBeParsed
        for service in self.parser.parse_line():
            instance = self.__create_service(service)
            self.service_injector.service_consumer.register_service(
                service.identifier,
                instance
            )

    def __create_service(self, service_definition) -> object:
        class_name, module = ServiceRecorder.__separate_class_and_module(
            service_definition.class_path
        )
        new_instance = ServiceRecorder.__generate_instance(
            module,
            class_name,
            self.__to_instance(service_definition.dependencies) # get dependency instances
        )
        return Service(
            service_definition.identifier,
            new_instance,
            service_definition.tag
        )

    def __to_instance(self, dependencies = []):
        return [
            self.service_injector.get_service(dependency).instance for dependency in dependencies
        ]


    @staticmethod
    def __separate_class_and_module(full_path) -> tuple:
        last_separator_char = full_path.rfind('.')
        class_name = full_path[last_separator_char + 1:]
        module_name = full_path[:last_separator_char]
        return class_name, module_name

    @staticmethod
    def __requires_initialisation(instance) -> bool:
        method = getattr(instance, '__init__', None)
        return callable(method) is not None

    @staticmethod
    def __get_class(module_name, class_name):
        parts = module_name.split('.')
        module_reference = __import__(module_name)
        parts.append(class_name)
        for folder in parts[1:]:
            module_reference = getattr(module_reference, folder)
        return module_reference

    @staticmethod
    def __generate_instance(module_name, class_name, args=None) -> object:
        return ServiceRecorder.__get_class(module_name, class_name)(*args)


class Service(dict):
    """
    Shape of a service that will be consume by the DependencyConsumer
    """

    def __init__(self, identifier, instance, tags):
        super(Service, self).__init__()
        self.identifier = identifier
        self.instance = instance
        self.tags = tags


class ServiceFileParser:
    """
    Abstract class that defines the methods that are required for a parser to be
    implemented
    """

    def __init__(self):
        self.file = None

    def set_filepath(self, file):
        """
        :param file: The file location to be parsed
        """
        self.file = file

    def can_be_parsed(self) -> bool:
        """
        :return: If the file can be processed by the parser
        """
        raise NotImplementedError

    def parse_line(self) -> object:
        """
        Reads the definition file, and creates a list of objects containing the
        instances

        :return: A generator of ServiceDefinition
        """
        raise NotImplementedError


class YamlServiceFileParser(ServiceFileParser):
    """
    Parses a YAML service definition file
    """

    def can_be_parsed(self) -> bool:
        return self.file.endswith('yaml') or self.file.endswith('yml')

    def parse_line(self) -> Generator:
        with open(self.file, mode='r') as definition_file:
            service_declarations = load(definition_file.read(), Loader)
            for (service_id, definition) in service_declarations['services'].items():
                yield self.__transform_service_definition(service_id, definition)

    @staticmethod
    def __transform_service_definition(service_id, definition) -> object:
        service_definition = ServiceDefinition(
            service_id,
            definition['class']
        )
        if 'arguments' in definition:
            for dependency in definition['arguments']:
                service_definition.add_dependency(dependency)

        if 'tag' in definition:
            for key, value in definition['tag'].items():
                service_definition.add_tag(key, value)
        return service_definition


class ServiceDefinition:
    """
    Represents a service
    """

    def __init__(self, identifier, class_path):
        """
        :param identifier: An unique identifier for the service
        :param class_path: The location of the class `module_1.module_n.ClassName`
        """
        self.identifier = identifier
        self.class_path = class_path
        self.dependencies = []
        self.tag = {}

    def add_dependency(self, identifier) -> None:
        """
        Adds a dependency to this service

        :param identifier: The identifier of the dependency
        """
        if identifier in self.dependencies:
            raise DependencyAlreadyExists
        self.dependencies.append(identifier)

    def add_tag(self, key, value) -> None:
        """
        Adds a tag to a ServiceDefinition to be managed by an external service

        :param key: Key of the property
        :param value: Value of the property
        """
        self.tag[key] = value


class ServiceAlreadyExists(Exception):
    """
    A service has been already been registered
    """


class ServiceDoesNotExist(Exception):
    """
    A service does not exist
    """


class DependencyAlreadyExists(Exception):
    """
    A dependency is already been registered in a service
    """


class FileCannotBeParsed(Exception):
    """
    A file is incompatible with a parser
    """
