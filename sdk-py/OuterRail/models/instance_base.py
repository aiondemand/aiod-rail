import json
from typing_extensions import Self
from typing import Any, ClassVar, Dict, List, Optional, Callable
from pydantic import BaseModel, StrictBool, StrictStr, ConfigDict

from OuterRail import Configuration, ApiClient, ExperimentTemplatesApi
from OuterRail.models.task_type import TaskType
from OuterRail.models.asset_schema import AssetSchema
from OuterRail.models.environment_var_def import EnvironmentVarDef

class AlreadyDeletedError(Exception):
    def __init__(self, message="This object has already been deleted", object_type=None):
        super().__init__(message)
        self.object_type = object_type
        self.message = message

    def __str__(self):
        if self.object_type:
            return f"{self.message} (Object type: {self.object_type})"
        return self.message


class Instance(BaseModel):

    """
        AIoD - RAIL

        Instance Base class

        This implements methods and decorators used by multiple instance subclasses.
    """

    def handle_deleted(func: Callable) -> Callable:
        """
        Decorator that handles deletion of an instance.

        Args:
            Implicit by decorator use

        Returns:
            Callable: a wrapper function that handles deletion of an instance.

        Raises:
            AlreadyDeletedError: if the instance is already deleted.
        """
        def wrapper(self, *args, **kwargs) -> None:
            if (self, '_deleted', False):
                raise AlreadyDeletedError(object_type=self)
            return func(self, *args, **kwargs)
        return wrapper


    # def delete(self) -> None:
    #     """
    #     Deletes the experiment template.
    #
    #     Returns:
    #         None.
    #
    #     Raises:
    #         ApiException: In case of a failed HTTP request.
    #     """
    #     with ApiClient(self._config) as api_client:
    #         api_instance = ExperimentTemplatesApi(api_client)
    #         try:
    #             api_instance.remove_experiment_template_v1_experiment_templates_id_delete(id=self.id)
    #             self._deleted = True
    #         except Exception as e:
    #             raise e
    #
    # def _set_config(self, config: Configuration) -> None:
    #     """
    #     Sets the configuration of the experiment template required for API calls.
    #
    #     Args:
    #     config (Configuration): The api configuration.
    #
    #     Returns:
    #         None:
    #     """
    #     self._config = config
    #
    # @classmethod
    # def from_json(cls, json_str: str) -> Optional[Self]:
    #     """
    #     Creates an instance of ExperimentTemplateCreate from a JSON string.
    #
    #     Args:
    #         json_str: The JSON string to create the instance from.
    #
    #     Returns:
    #         ExperimentTemplate: Instance of ExperimentTemplate.
    #     """
    #     return cls.from_dict(json.loads(json_str))
    #
    # @classmethod
    # def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
    #     pass
    #
    # @staticmethod
    # def build_creation_dict(template: dict | tuple[str, str, str, dict]):
    #     pass