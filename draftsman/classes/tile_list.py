# tilelist.py

from draftsman.tile import Tile, new_tile
from draftsman.data import tiles
from draftsman.error import DataFormatError, InvalidTileError

from collections.abc import MutableSequence
from copy import deepcopy
from typing import Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no coverage
    from draftsman.classes.collection import TileCollection


class TileList(MutableSequence):
    """
    TODO
    """

    def __init__(
        self,
        parent: "TileCollection",
        initlist: Optional[list[Tile]] = None,
        if_unknown: str = "error",  # TODO: enum
    ) -> None:
        """
        TODO
        """
        self.data = []
        self._parent = parent
        if initlist is not None:
            for elem in initlist:
                if isinstance(elem, Tile):
                    self.append(elem, if_unknown=if_unknown)
                elif isinstance(elem, dict):
                    name = elem.pop("name")
                    self.append(name, **elem, if_unknown=if_unknown)
                else:
                    raise DataFormatError(
                        "TileList only takes either Tile or dict entries"
                    )

    def append(
        self,
        name: Union[str, Tile],
        copy: bool = True,
        merge: bool = False,
        if_unknown: str = "error",  # TODO: enum
        **kwargs
    ) -> None:
        """
        Appends the Tile to the end of the sequence.

        TODO
        """
        self.insert(
            idx=len(self),
            name=name,
            copy=copy,
            merge=merge,
            if_unknown=if_unknown,
            **kwargs
        )

    def insert(
        self,
        idx: int,
        name: Union[str, Tile],
        copy: bool = True,
        merge: bool = False,
        if_unknown: str = "error",  # TODO: enum
        **kwargs
    ) -> None:
        """
        Inserts an element into the TileList.

        TODO
        """
        # Convert to new Entity if constructed via string keyword
        new = False
        if isinstance(name, str):
            tile = new_tile(name, **kwargs, if_unknown=if_unknown)
            if tile is None:
                return
            new = True
        else:
            tile = name

        if copy and not new:
            # Create a DEEPcopy of the entity if desired
            tile = deepcopy(tile)
            # Overwrite any user keywords if specified in the function signature
            for k, v in kwargs.items():
                setattr(tile, k, v)

        # If we attempt to merge an tile that isn't a copy, bad things will
        # probably happen
        # Not really sure what *should* happen in that case, so lets just nip
        # that in the bud for now
        if not copy and merge:
            raise ValueError(
                "Attempting to merge a non-copy, which is disallowed (for now at least)"
            )

        # Check tile
        if not isinstance(tile, Tile):
            raise TypeError("Entry in TileList must be a Tile")

        if self._parent:
            tile = self._parent.on_tile_insert(tile, merge)

        if tile is None:  # Tile was merged
            return  # Don't add this tile to the list

        # Manage TileList
        self.data.insert(idx, tile)

        # Keep a reference of the parent blueprint in the tile
        tile._parent = self._parent

    def union(self, other: "TileList") -> "TileList":
        """
        TODO
        """
        new_tile_list = TileList(None)

        for tile in self.data:
            new_tile_list.append(tile)
            new_tile_list[-1]._parent = None

        for other_tile in other.data:
            already_in = False
            for tile in self.data:
                if tile == other_tile:
                    already_in = True
                    break
            if not already_in:
                new_tile_list.append(other_tile)

        return new_tile_list

    def intersection(self, other: "TileList") -> "TileList":
        """
        TODO
        """
        new_tile_list = TileList(None)

        for tile in self.data:
            in_both = False
            for other_tile in other.data:
                if other_tile == tile:
                    in_both = True
                    break
            if in_both:
                new_tile_list.append(tile)

        return new_tile_list

    def difference(self, other: "TileList") -> "TileList":
        # type: (TileList) -> TileList
        """
        TODO
        """
        new_tile_list = TileList(None)

        for tile in self.data:
            different = True
            for other_tile in other.data:
                if other_tile == tile:
                    different = False
                    break
            if different:
                new_tile_list.append(tile)

        return new_tile_list

    def __getitem__(self, idx: Union[int, slice]) -> Union[Tile, list[Tile]]:
        return self.data[idx]

    def __setitem__(self, idx: int, value: Tile) -> None:
        # TODO: handle slices
        # Check tile
        if not isinstance(value, Tile):
            raise TypeError("Entry in TileList must be a Tile")

        # Handle parent
        self._parent.on_tile_set(self.data[idx], value)

        # Manage the TileList
        self.data[idx] = value

        # Add a reference to the container in the object
        value._parent = self._parent

    def __delitem__(self, idx: Union[int, slice]) -> None:
        if isinstance(idx, slice):
            # Get slice parameters
            start, stop, step = idx.indices(len(self))
            for i in range(start, stop, step):
                # Remove from parent
                self._parent.on_tile_remove(self.data[i])
        else:
            self._parent.on_tile_remove(self.data[idx])

        # Remove from self
        del self.data[idx]

    def __len__(self) -> int:
        return len(self.data)

    def __or__(self, other: "TileList") -> "TileList":
        # TODO: NotImplemented
        return self.union(other)

    # def __ior__(self, other: "TileList") -> None:
    #     self.union(other)

    def __and__(self, other: "TileList") -> "TileList":
        # TODO: NotImplemented
        return self.intersection(other)

    # def __iand__(self, other: "TileList") -> None:
    #     self.intersection(other)

    def __sub__(self, other: "TileList") -> "TileList":
        # TODO: NotImplemented
        return self.difference(other)

    # def __isub__(self, other: "TileList") -> None:
    #     self.difference(other)

    def __eq__(self, other: "TileList") -> bool:
        # TODO: not implmented
        if not isinstance(other, TileList):
            return False
        # if len(self.data) != len(other.data):
        #     return False
        # for i in range(len(self.data)):
        #     if self.data[i] != other.data[i]:
        #         return False
        # return True
        return self.data == other.data

    def __repr__(self) -> str:  # pragma: no coverage
        return "<TileList>{}".format(self.data)

    # @classmethod
    # def __get_pydantic_core_schema__(
    #     cls, _source_type: Any, handler: GetCoreSchemaHandler
    # ) -> CoreSchema:
    #     return core_schema.no_info_after_validator_function(
    #         cls, handler(list[Tile])
    #     )  # TODO: correct annotation
