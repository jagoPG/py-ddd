# PYTHON DOMAIN DRIVEN DESIGN TEMPLATE
This is a custom implementation of DDD pattern with *Python 3*. Some other patters are used to
ease the clarity of the code, such as *Dependency Injection*, *Command Bus*, *Data Transformer*...

# REQUIREMENTS
* Python 3
* VirtualEnv

# INSTALLATION
There is a `bin/bash` directory at the root folder with all tasks defined:
```
./bin/bash/init.sh
```

# RUN APP
```
./bin/bash/run.sh && open http://127.0.0.1:5000
```


# TEST EXECUTION
```
./bin/bash/test.sh
```

# APP FOLDER STRUCTURE
## Application
Commands, queries, data transformers... glue between business logic and application infrastructure.

## Domain
Business logic of the application.

### Events
Subscribers to domain root published events.

### Model
Domain abstraction, main business logic.

## Infrastructure
Controller layer framework, configuration, integration of internal services with third party
libraries, application control, application utilities...

# WORKFLOW
To make new contributions open a new *Pull request* in the repository or an issue with the
suggestion - a PR is preferred. Make sure that your code has implemented enough tests, is not
breaking any existing code, is properly documented and fulfills the code style.

## Test naming
Tests are stored in the `test` folder located at the root directory of the project. The name of
each file module should start by `test_`, followed by the name of the module that it is testing, or
a meaningful name.

## Launch Python linter
```
./bin/bash/lint.sh
```
