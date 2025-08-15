## 2025-08-15 Ian Laird <irlaird@gmail.com>

Contributions for release 1.6.3

- Adding support flag for python 3.11, 3.12.

## 2023-09-28 Ian Laird <irlaird@gmail.com>

Contributions for release 1.6.1

- Fixed typeo in readme.
- Added github jobs to lint and unittest code.
- Fixed styling and flake8 issues.

## 2023-09-28 Ian Laird <irlaird@gmail.com>

Contributions for release 1.6.0

- Improved the message of the KeyError exception thrown when a bound member is
  not found and created a custom exception, MemberNotBoundError, that is thrown
  in these cases. Callers can catch either KeyError or MemberNotBoundError.
- Added unittests to ensure KeyError and MemberNotBoundErrors are both catchable
  in these cases.
- Add missing docstrings to other parts of the code.
- Updated Readme to include examples of builder and autowire apis.
- Added CHANGELOG.md to the project to document changes.

## 2023-09-27 Ian Laird <irlaird@gmail.com>

Contributions for release 1.6.0

- Added autowire module to support decorator-based ioc configuration.
- Added test suites to verify functionality of autowire modules.

## 2023-08-27 Ian Laird <irlaird@gmail.com>

Contributions for release 1.5.0

- Addressed consistency issues between the BuilderBase and
  StaticContainerBuilder interface. Backward compatability has been maintained.
- Updated Examples to use call chaining

## 2023-08-26 Ian Laird <irlaird@gmail.com>

Contributions for release 1.5.0

- Added a BuilderBase class that wraps the StaticContainerBuilder that makes
  using the Builder Pattern with PyIOC3 easier.
- Added a optional argument to the StaticContainerBuilder that allows the caller
  to pass in default bindings.
- Refactored the StaticContainerBuilder to use FactoryBinding, ConstantBinding,
  and ProviderBinding internally.
- Updated Readme
