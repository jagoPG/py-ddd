
class SimpleBus:
    """
    Searches an appropriate handler for a command
    """

    def __init__(self):
        self.operation_provider = OperationProvider()

    def execute(self, operation):
        """
        Searches a handler and launches the command

        :param operation: a DTO class
        """
        module_name = operation.__class__.__module__
        class_name = operation.__class__.__name__
        handler = self.__get_handler(
            '{0}.{1}'.format(module_name, class_name)
        )
        return handler.invoke(operation)

    def __get_handler(self, command_class) -> object:
        if not self.operation_provider.is_operation(command_class):
            raise HandlerNotFound
        return self.operation_provider.operations[command_class]


class OperationProvider:
    def __init__(self):
        self.operations = {}

    def record(self, dto_class, handler) -> None:
        """
        Records a operation handler in the bus

        :param dto_class: <module>.<class> full qualifier
        :param handler: instance of the service which will handle the request
        """
        identifier = '{0}.{1}'.format(dto_class.__module__, dto_class.__name__)
        if identifier in self.operations:
            raise HandlerAlreadyExists
        self.operations[identifier] = handler

    def is_operation(self, operation_class) -> bool:
        """
        :param operation_class: The classname as string
        :return: If the operation is already registered
        """
        return operation_class in self.operations


class OperationHandler:
    """
    Definition of the methods a handler must implement
    """

    def invoke(self, operation):
        """
        Executes the operation

        :param operation: DTO with data
        """
        raise NotImplementedError()


class HandlerNotFound(Exception):
    """
    This exception has to be raised if a handler is not found
    """


class HandlerAlreadyExists(Exception):
    """
    A handler has already be defined
    """
