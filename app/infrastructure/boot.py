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
        logging.info(vars(self.injector.service_consumer))

    def __setup_logging(self):
        logging.basicConfig(
            format='%(process)d-%(levelname)s-%(message)s',
            level=logging.INFO,
            stream=sys.stdout
        )
