from __future__ import annotations

import json
import pprint
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set, Union
from pydantic import BaseModel, ConfigDict, StrictBool, StrictFloat, StrictInt, StrictStr
from typing_extensions import Self

from OuterRail import EnvironmentVar, Configuration

"""
    AIoD - RAIL

    Experiment class. 
    
    Implementation of class representing an instance of experiment and methods
    operating with this instance.
"""


class Experiment(BaseModel):
    id: StrictStr
    name: StrictStr
    description: StrictStr
    experiment_template_id: StrictStr
    is_mine: StrictBool
    is_public: StrictBool
    is_archived: StrictBool
    created_at: datetime
    updated_at: datetime
    model_ids: List[StrictStr]
    dataset_ids: List[StrictStr]
    env_vars: List[EnvironmentVar]
    publication_ids: Optional[List[StrictStr]] = None
    __properties: ClassVar[List[str]] = [
        "name", "description", "is_public", "experiment_template_id", "dataset_ids", "model_ids", "publication_ids",
        "env_vars", "id", "created_at", "updated_at", "is_archived", "is_mine"
    ]
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, protected_namespaces=())

    def _set_config(self, config: Configuration) -> None:
        """
        Sets the configuration of the experiment template required for API calls.

        Args:
        config (Configuration): The api configuration.

        Returns:
            None:
        """
        self._config = config

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]], config: Configuration = None) -> Optional[Self]:
        """
        Create an instance of ExperimentRunResponse from a dict

        Args:
            obj (Optional[Dict[str, Any]]): Obj representing the experiment in either a dictionary or
            an already existing instance.
            config (:obj:`Configuration`, optional): The api configuration. Defaults to None.

        Returns:
            None: If input arg "obj" is None.
            Experiment: In successful conversion from dict.
        """
        if obj is None:
            return None
        _obj = cls.model_validate(obj)
        if config is not None:
            _obj._set_config(config)
        return _obj

