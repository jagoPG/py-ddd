class DependencyInjector:
    """
    Provides access to registered services
    """

    def __init__(self, name, version):
        """
        :param name: Name of the dependency injector
        :param version: Version of the dependency injector
        """
        self.name = name
        self.version = version
        self.service_consumer = DependencyConsumer()

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


class DependencyConsumer:
    """
    Stores the services of the dependency injector
    """

    def __init__(self):
        self.services = {}

    def register_service(self, identifier, service):
        """
        Registers a service in the DependencyInjector

        :param identifier: An unique identifier for the service
        :param service: An instance of the service
        :raises: ServiceAlreadyExists
        """
        if identifier in self.services:
            raise ServiceAlreadyExists
        self.services[identifier] = service


class ServiceAlreadyExists(Exception):
    """
    A service has been already been registered
    """


class ServiceDoesNotExist(Exception):
    """
    A service does not exist
    """
