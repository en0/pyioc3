from enum import Enum
from .errors import ScopeError


class ScopeEnum(Enum):
    """
    ScopeEnum is an enumeration class representing different dependency scopes.

    Attributes:
        TRANSIENT (ScopeEnum): Indicates a transient scope where a new instance is
            created for each request.
        REQUESTED (ScopeEnum): Indicates a requested scope where a single instance is
            created for the duration of a request, typically used in web applications.
        SINGLETON (ScopeEnum): Indicates a singleton scope where a single instance is
            created and shared across the entire application.

    Methods:
        from_string(val: str) -> "ScopeEnum":
            Converts a string representation of a scope to a ScopeEnum value.

    Example:
        To use `ScopeEnum` to represent a scope in your code:

        ```python
        from pyioc3.scope_enum import ScopeEnum

        # Define a variable with a ScopeEnum value.
        my_scope = ScopeEnum.TRANSIENT

        # Convert a string to a ScopeEnum value.
        scope_string = "singleton"
        scope_enum = ScopeEnum.from_string(scope_string)
        ```

    See Also:
        - `errors.ScopeError`: Error raised when an unknown scope string is provided
          to the `from_string` method.

    """

    TRANSIENT = 1
    REQUESTED = 2
    SINGLETON = 3

    @staticmethod
    def from_string(val: str) -> "ScopeEnum":
        """
        Converts a string representation of a scope to a ScopeEnum value.

        Args:
            val (str): A string representing a scope, such as "transient," "requested,"
                or "singleton."

        Returns:
            ScopeEnum: The corresponding ScopeEnum value.

        Raises:
            ScopeError: If the provided string does not match any known scope.

        Example:
            To convert a string to a ScopeEnum value:

            ```python
            from pyioc3.scope_enum import ScopeEnum

            # Convert a string to a ScopeEnum value.
            scope_string = "singleton"
            scope_enum = ScopeEnum.from_string(scope_string)
            ```
        """
        try:
            return {
                "TRANSIENT": ScopeEnum.TRANSIENT,
                "REQUESTED": ScopeEnum.REQUESTED,
                "SINGLETON": ScopeEnum.SINGLETON,
                "transient": ScopeEnum.TRANSIENT,
                "requested": ScopeEnum.REQUESTED,
                "singleton": ScopeEnum.SINGLETON,
                "t": ScopeEnum.TRANSIENT,
                "r": ScopeEnum.REQUESTED,
                "s": ScopeEnum.SINGLETON,
                "T": ScopeEnum.TRANSIENT,
                "R": ScopeEnum.REQUESTED,
                "S": ScopeEnum.SINGLETON,
            }[val]

        except KeyError as ex:
            raise ScopeError(f'Unknown scope "{val}"') from ex
