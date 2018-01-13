# Contributing
You are here to help on **SQLAlchemy DST**? Awesome, feel welcome and read the following sections to know what and how to work on something. 

It's an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into **SQLAlchemy DST** itself.

## Code of Conduct
All members of our community are expected to follow our [Code of Conduct](https://github.com/yarbshk/sqlalchemy-dst/blob/master/CODE_OF_CONDUCT.md). Please make sure you are welcoming and friendly in all of our spaces.

## Issues
Before you submit an issue, please **search the issue tracker**, maybe an issue for your problem already exists and the discussion might inform you of workarounds readily available.

We want to fix all the issues as soon as possible, but before fixing a bug we need to reproduce and confirm it. In order to reproduce bugs we ask you to **provide a minimal reproduction scenario** that include:
- Version of the module used.
- Environment information (3rd-party libraries, technology stack etc.).
- **A use-case that fails!**

If you get stuck at any point you can create a [ticket on GitHub](https://github.com/yarbshk/sqlalchemy-dst/issues).

## Pull requests
**Working on your first Pull Request?** You can learn how from this free series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

If you would make PR for something that is bigger than a one or two line fix:
1. Create your own fork of the code.
2. **Before start development** be sure you are following:
    - Our [Code of Conduct](https://github.com/yarbshk/sqlalchemy-dst/blob/master/CODE_OF_CONDUCT.md).
    - [The documented overview](https://github.com/yarbshk/sqlalchemy-dst) to have a particular road map.
    - The code style for the project (please use [PEP-8](https://www.python.org/dev/peps/pep-0008/)).
    - Commit message convention (sentence case, present time).
3. Do the changes in your fork.
4. **Write one or more tests** for all features or bug fixes.
5. Provide documentation for all public API methods.
6. Only **if you like the change** and think **the project could use it**:
    - Send a pull request.
    
## Getting started
To **run the project for testing** use the following micro guide:
1. Get local copy of the project.
2. Be sure that [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.
3. Rename the `.env-example` file (must be simply `.env`) in project root.
4. Go to the project root in your terminal and execute the `docker-compose up` command to see the unittest module in action.

If you finish the guide you will be able to develop and test the app. Good luck!
