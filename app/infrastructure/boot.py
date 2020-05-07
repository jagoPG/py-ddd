from infrastructure.domain_events import DomainEventPublisher
from infrastructure.service_injector import ServiceInjector, ServiceRecorder, YamlServiceFileParser
import logging
import sys


class Boot:
    SERVICE_DEFINITION_DIR = 'app/infrastructure/config/services.yaml'

    def __init__(self):
        self.injector = ServiceInjector('default', '1.0')
        self.parser = YamlServiceFileParser()

    def start(self):
        self.__setup_logging()
        recorder = ServiceRecorder(self.injector, self.parser)
        recorder.record(Boot.SERVICE_DEFINITION_DIR)
        self.__setup_domain_event_subscribers()
        logging.info(vars(self.injector.service_consumer))

    def __setup_logging(self):
        logging.basicConfig(
            format='%(module)s.%(filename)s:%(lineno)d [%(levelname)s] %(message)s',
            level=logging.DEBUG,
            stream=sys.stdout
        )

    def __setup_domain_event_subscribers(self):
        for (id, service) in self.injector.service_consumer.services.items():
            for tag in service.tags:
                if tag['name'] == 'domain_event_sub':
                    DomainEventPublisher.get_instance().subscribe(
                        service.identifier,
                        service.instance
                    )
