# linked_belt.py

from draftsman.classes.entity import Entity
from draftsman.classes.mixins import DirectionalMixin
from draftsman.error import DraftsmanError
from draftsman.classes.vector import Vector, PrimitiveVector
from draftsman.constants import Direction, ValidationMode

from draftsman.data.entities import linked_belts

from pydantic import ConfigDict
from typing import Any, Literal, Union

try:  # pragma: no coverage
    default_linked_belt = linked_belts[0]
except IndexError:  # pragma: no coverage
    default_linked_belt = None


class LinkedBelt(DirectionalMixin, Entity):
    """
    A belt object that can transfer items over any distance, regardless of
    constraint, as long as the two are paired together.

    .. WARNING::

        Functionally, currently unimplemented. Need to analyze how mods use this
        entity, as I can't seem to figure out the example one in the game.
    """

    class Format(DirectionalMixin.Format, Entity.Format):
        model_config = ConfigDict(title="LinkedBelt")

    def __init__(
        self,
        name: str = linked_belts[0],
        position: Union[Vector, PrimitiveVector] = None,
        tile_position: Union[Vector, PrimitiveVector] = (0, 0),
        direction: Direction = Direction.NORTH,
        tags: dict[str, Any] = {},
        validate: Union[
            ValidationMode, Literal["none", "minimum", "strict", "pedantic"]
        ] = ValidationMode.STRICT,
        validate_assignment: Union[
            ValidationMode, Literal["none", "minimum", "strict", "pedantic"]
        ] = ValidationMode.STRICT,
        **kwargs
    ):
        """
        TODO
        """

        # TODO: this should be better
        if len(linked_belts) == 0:  # pragma: no coverage
            raise DraftsmanError(
                "There is no LinkedBelt to create; check your Factorio version"
            )

        super().__init__(
            name,
            linked_belts,
            position=position,
            tile_position=tile_position,
            direction=direction,
            tags=tags,
            **kwargs
        )

        self.validate_assignment = validate_assignment

        self.validate(mode=validate).reissue_all(stacklevel=3)

    # =========================================================================

    __hash__ = Entity.__hash__
