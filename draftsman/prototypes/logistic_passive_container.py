# logistic_passive_container.py

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import (
    RequestItemsMixin,
    LogisticModeOfOperationMixin,
    CircuitConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    InventoryMixin,
)
from draftsman.classes.vector import Vector, PrimitiveVector
from draftsman.constants import ValidationMode
from draftsman.data.entities import of_type
from draftsman.signatures import ItemRequest, uint16
from draftsman.utils import get_first

from draftsman.data.entities import logistic_passive_containers

from typing import Any, Literal, Optional, Union
from pydantic import ConfigDict


class LogisticPassiveContainer(
    InventoryMixin,
    RequestItemsMixin,
    LogisticModeOfOperationMixin,
    CircuitConditionMixin,
    ControlBehaviorMixin,
    CircuitConnectableMixin,
    Entity,
):
    """
    A logistics container that provides it's contents to the logistic network
    when needed by the network.
    """

    class Format(
        InventoryMixin.Format,
        RequestItemsMixin.Format,
        LogisticModeOfOperationMixin.Format,
        CircuitConditionMixin.Format,
        ControlBehaviorMixin.Format,
        CircuitConnectableMixin.Format,
        Entity.Format,
    ):
        class ControlBehavior(
            LogisticModeOfOperationMixin.ControlFormat,
            CircuitConditionMixin.ControlFormat,
        ):
            pass

        control_behavior: Optional[ControlBehavior] = ControlBehavior()

        model_config = ConfigDict(title="LogisticPassiveContainer")

    def __init__(
        self,
        name: Optional[str] = get_first(logistic_passive_containers),
        position: Union[Vector, PrimitiveVector] = None,
        tile_position: Union[Vector, PrimitiveVector] = (0, 0),
        bar: uint16 = None,
        items: Optional[list[ItemRequest]] = [],
        control_behavior: Optional[Format.ControlBehavior] = {},
        tags: dict[str, Any] = {},
        validate_assignment: Union[
            ValidationMode, Literal["none", "minimum", "strict", "pedantic"]
        ] = ValidationMode.STRICT,
        **kwargs
    ):
        super().__init__(
            name,
            logistic_passive_containers,
            position=position,
            tile_position=tile_position,
            bar=bar,
            items=items,
            control_behavior=control_behavior,
            tags=tags,
            **kwargs
        )

        self.validate_assignment = validate_assignment

    # =========================================================================

    __hash__ = Entity.__hash__
