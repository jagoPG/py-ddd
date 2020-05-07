from application.persist_event import PersistEventCommand
from infrastructure.boot import Boot
import logging

if __name__ == '__main__':
    app = Boot()
    app.start()
    handler = app.injector.get_service(
        'app.application.command.persist_event'
    )
    handler.instance.handle(
        PersistEventCommand('123', 'My Sweet Torment - TLBH route in O2 Arena')
    )
    repository = app.injector.get_service(
        'app.persistence.sql.event_repository'
    )
    logging.info(repository.instance.of_id('123'))
