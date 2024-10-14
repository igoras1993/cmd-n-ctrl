# Command and Control

App exposes UI for managing my personal stuff.

## Prerequisites

### Python 3.12

This project uses python3.12. It is very likely that You do not have it installed on Your machine.

#### Debian/Ubuntu/Mint/...

The simplest method is to install pre-built binaries:

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-dev libpq-dev
```

#### MacOS

Download installer from [python website](https://www.python.org/downloads/macos/)

### pipx

[`pipx`](https://pipx.pypa.io/stable/) is a tool to help you install and run end-user applications written in Python. It's roughly similar to macOS's brew, JavaScript's npx, and Linux's apt.

#### Debian/Ubuntu/Mint

```shell
sudo apt update
```

* Install via pip
```
python3.12 -m pip install --user pipx
python3 -m pipx ensurepath
```

* Install via apt (only if you are sure that `python --version` == `3.12`)
```
sudo apt install pipx
pipx ensurepath
```

#### MacOS

```shell
brew install pipx
pipx ensurepath
```

### Poetry

This project manages it's dependencies using [poetry](https://python-poetry.org/docs/)

#### MacOS + Linux

```shell
pipx install poetry
```

## Repository setup

Configures Poetry to create virtual environments within the project directory, specifically inside a .venv directory:

```shell
poetry config virtualenvs.in-project true
```

Setup Your repository and environment with:

```shell
make init
```

This will install git hooks and will create poetry environ with all `dev` and `test` dependencies.

## Usage

### Setup test/development database

```shell
make test-db
```

### Setup head db revision

```shell
make migrate-head
```

### Run development server

```shell
make asgi
```

### Run test suite

```shell
make test
```

### Autogenerate new migration

```shell
make migrate-generate MESSAGE="Your revision message"
```

### Others

See predefined commands in `Makefile` for more.

## Contributing

### Commits
All commits should be structured according to [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/).

For answer "Which one commit type should I use?", please refer to below table.

#### Commit types

| Commit Type | Title                    | Description                                                                                                 |
|:-----------:|--------------------------|-------------------------------------------------------------------------------------------------------------|
|   `feat`    | Features                 | A new feature                                                                                               |
|    `fix`    | Bug Fixes                | A bug Fix                                                                                                   |
|   `docs`    | Documentation            | Documentation only changes                                                                                  |
|   `style`   | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)      |
| `refactor`  | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
|   `perf`    | Performance Improvements | A code change that improves performance                                                                     |
|   `test`    | Tests                    | Adding missing tests or correcting existing tests                                                           |
|   `build`   | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
|    `ci`     | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
|   `chore`   | Chores                   | Other changes that don't modify src or test files                                                           |
|  `revert`   | Reverts                  | Reverts a previous commit                                                                                   |

Source: https://github.com/pvdlg/conventional-changelog-metahub/blob/master/README.md#commit-types

### Changelog
Changelog is generated automatically using [git-cliff](https://git-cliff.org/docs/usage/exampleshttps://git-cliff.org/docs/usage/examples)

If you want to add new changes to CHANGELOG.md run:
```
git cliff -o
```

## Notes

### Rpi controllers
- https://github.com/rpi-ws281x/rpi-ws281x-python/tree/master
