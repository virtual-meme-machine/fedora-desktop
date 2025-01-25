import dataclasses

import data.OperationType as OperationType


@dataclasses.dataclass
class Action:
    """
    Defines a single action preformed by an option
    :param operation_type: Type of operation that will be performed, eg: OperationType.PACKAGE_REMOVE
    :param operation_args: Arguments that should be passed to the operation, eg: ["firefox"]
    """
    operation_type: OperationType.OperationType
    operation_args: list

    @classmethod
    def from_dict(cls, action_dict: dict):
        """
        Loads an Action from a provided dictionary
        :param action_dict: Dictionary containing serialized Action data
        :return: Loaded Action object
        """
        return Action(operation_type=OperationType.from_string(action_dict.get("operation_type")),
                      operation_args=action_dict.get("operation_args"))
