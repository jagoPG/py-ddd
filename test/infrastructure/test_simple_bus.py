from unittest import TestCase
from unittest.mock import MagicMock

from app.infrastructure.simple_bus import OperationHandler, SimpleBus, HandlerNotFound, \
    HandlerAlreadyExists


class MyOperationCommand:
    """
    Just a DTO for `MyOperationHandler
    """


class MyNonRegisteredCommand:
    """
    Just a DTO that won't have a handler
    """


class MyOperationHandler(OperationHandler):
    def invoke(self, operation):
        return True


class SimpleBusTest(TestCase):
    def setUp(self) -> None:
        self.simple_bus = SimpleBus()

    def test_operation_is_recorded(self):
        handler = MyOperationHandler()
        expected = {}
        expected_class = '{0}.{1}'.format(
            MyOperationCommand.__module__, MyOperationCommand.__name__
        )
        expected[expected_class] = handler
        self.simple_bus.operation_provider.record(
            MyOperationCommand,
            handler
        )
        self.assertEqual(expected, self.simple_bus.operation_provider.operations)

    def test_operation_is_not_recorded(self):
        with self.assertRaises(HandlerNotFound):
            self.simple_bus.execute(MyNonRegisteredCommand())

    def test_operation_is_already_recorded(self):
        handler = MyOperationHandler()
        self.simple_bus.operation_provider.record(
            MyOperationCommand,
            handler
        )
        with self.assertRaises(HandlerAlreadyExists):
            other_handler = MyOperationHandler
            self.simple_bus.operation_provider.record(
                MyOperationCommand,
                other_handler
            )

    def test_operation_can_be_executed(self):
        handler = MyOperationHandler()
        handler.invoke = MagicMock()
        command = MyOperationCommand()
        self.simple_bus.operation_provider.record(
            MyOperationCommand,
            handler
        )
        self.simple_bus.execute(command)
        handler.invoke.assert_called_with(command)

    def test_operation_exists(self):
        handler = MyOperationHandler()
        self.simple_bus.operation_provider.record(
            MyOperationCommand,
            handler
        )
        identifier = '{0}.{1}'.format(
            MyOperationCommand.__module__, MyOperationCommand.__name__
        )
        self.assertTrue(
            self.simple_bus.operation_provider.is_operation(identifier)
        )
