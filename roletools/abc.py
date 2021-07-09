from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.commands import Context

from .converter import (
    ButtonStyleConverter,
    RawUserIds,
    RoleEmojiConverter,
    RoleHierarchyConverter,
    SelfRoleConverter,
)

if TYPE_CHECKING:
    from .buttons import ButtonRoleConverter
    from .select import SelectOptionRoleConverter, SelectRoleConverter


@commands.group()
@commands.guild_only()
async def roletools(self: commands.Cog, ctx: Context) -> None:
    """
    Role tools commands
    """
    pass


class RoleToolsMixin(ABC):
    """
    Base class for well behaved type hint detection with composite class.

    Basically, to keep developers sane when not all attributes are defined in each mixin.
    """

    c = roletools

    def __init__(self, *_args):
        self.config: Config
        self.bot: Red
        self.settings: Dict[Any, Any]
        self._ready: asyncio.Event

    #######################################################################
    # roletools.py                                                        #
    #######################################################################

    @abstractmethod
    def update_cooldown(
        self, ctx: Context, rate: int, per: float, _type: commands.BucketType
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def initalize(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def selfrole(self, ctx: Context, *, role: SelfRoleConverter) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def selfrole_remove(self, ctx: Context, *, role: SelfRoleConverter) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def giverole(
        self,
        ctx: Context,
        role: RoleHierarchyConverter,
        *who: Union[discord.Role, discord.TextChannel, discord.Member, str],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def removerole(
        self,
        ctx: Context,
        role: RoleHierarchyConverter,
        *who: Union[discord.Role, discord.TextChannel, discord.Member, str],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def forcerole(
        self,
        ctx: Context,
        users: commands.Greedy[Union[discord.Member, RawUserIds]],
        *,
        role: RoleHierarchyConverter,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def forceroleremove(
        self,
        ctx: Context,
        users: commands.Greedy[Union[discord.Member, RawUserIds]],
        *,
        role: RoleHierarchyConverter,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def viewroles(self, ctx: Context, *, role: Optional[discord.Role]) -> None:
        raise NotImplementedError()

    #######################################################################
    # inclusive.py                                                        #
    #######################################################################

    @abstractmethod
    async def inclusive(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def inclusive_add(
        self, ctx: Context, role: RoleHierarchyConverter, *include: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def mutual_inclusive_add(self, ctx: Context, *roles: RoleHierarchyConverter) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def inclusive_remove(
        self, ctx: Context, role: RoleHierarchyConverter, *include: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    #######################################################################
    # exclusive.py                                                        #
    #######################################################################

    @abstractmethod
    async def exclusive(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def exclusive_add(
        self, ctx: Context, role: RoleHierarchyConverter, *exclude: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def mutual_exclusive_add(self, ctx: Context, *roles: RoleHierarchyConverter) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def exclusive_remove(
        self, ctx: Context, role: RoleHierarchyConverter, *exclude: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    #######################################################################
    # requires.py                                                         #
    #######################################################################

    @abstractmethod
    async def required_roles(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def required_add(
        self, ctx: Context, role: RoleHierarchyConverter, *required: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def required_remove(
        self, ctx: Context, role: RoleHierarchyConverter, *required: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    #######################################################################
    # settings.py                                                         #
    #######################################################################

    @abstractmethod
    async def selfadd(
        self, ctx: Context, true_or_false: Optional[bool] = None, *, role: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def selfrem(
        self, ctx: Context, true_or_false: Optional[bool] = None, *, role: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def atomic(self, ctx: Context, true_or_false: Optional[Union[bool, str]] = None) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def globalatomic(self, ctx: Context, true_or_false: Optional[bool] = None) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def sticky(
        self, ctx: Context, true_or_false: Optional[bool] = None, *, role: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def autorole(
        self, ctx: Context, true_or_false: Optional[bool] = None, *, role: RoleHierarchyConverter
    ) -> None:
        raise NotImplementedError()

    #######################################################################
    # reactions.py                                                        #
    #######################################################################

    @abstractmethod
    async def cleanup(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def ownercleanup(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def reactroles(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def clearreact(
        self,
        ctx: Context,
        message: discord.Message,
        *emojis: Optional[Union[discord.Emoji, str]],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def react(
        self,
        ctx: Context,
        message: discord.Message,
        emoji: Union[discord.Emoji, str],
        *,
        role: RoleHierarchyConverter,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def remreact(
        self,
        ctx: Context,
        message: discord.Message,
        *,
        role_or_emoji: Union[RoleHierarchyConverter, discord.Emoji, str],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def bulkreact(
        self,
        ctx: Context,
        message: discord.Message,
        *role_emoji: RoleEmojiConverter,
    ) -> None:
        raise NotImplementedError()

    #######################################################################
    # events.py                                                           #
    #######################################################################

    @abstractmethod
    async def check_guild_verification(
        self, member: discord.Member, guild: discord.Guild
    ) -> Union[bool, int]:
        raise NotImplementedError()

    @abstractmethod
    async def wait_for_verification(self, member: discord.Member, guild: discord.Guild) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def check_atomicity(self, guild: discord.Guild) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def give_roles(
        self,
        member: discord.Member,
        roles: List[discord.Role],
        reason: Optional[str] = None,
        *,
        check_required: bool = True,
        check_exclusive: bool = True,
        check_inclusive: bool = True,
        check_cost: bool = True,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def remove_roles(
        self,
        member: discord.Member,
        roles: List[discord.Role],
        reason: Optional[str] = None,
        *,
        check_inclusive: bool = True,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def _auto_give(self, member: discord.Member) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def _sticky_leave(self, member: discord.Member) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def _sticky_join(self, member: discord.Member) -> None:
        raise NotImplementedError()

    #######################################################################
    # buttons.py                                                          #
    #######################################################################

    @abstractmethod
    async def initialize_buttons(self):
        raise NotImplementedError()

    @abstractmethod
    async def send_buttons(
        self,
        ctx: Context,
        channel: discord.TextChannel,
        buttons: commands.Greedy[ButtonRoleConverter],
        *,
        message: str,
    ):
        raise NotImplementedError()

    @abstractmethod
    async def edit_with_buttons(
        self,
        ctx: Context,
        message: discord.Message,
        buttons: commands.Greedy[ButtonRoleConverter],
    ):
        raise NotImplementedError()

    @abstractmethod
    async def create_button(
        self,
        ctx: Context,
        name: str,
        role: RoleHierarchyConverter,
        label: Optional[str] = None,
        emoji: Optional[Union[discord.PartialEmoji, str]] = None,
        style: Optional[ButtonStyleConverter] = discord.ButtonStyle.primary,
    ):
        raise NotImplementedError()

    @abstractmethod
    async def delete_button(self, ctx: Context, *, name: str):
        raise NotImplementedError()

    @abstractmethod
    async def button_roles_view(self, ctx: Context) -> None:
        raise NotImplementedError()

    #######################################################################
    # select.py                                                           #
    #######################################################################

    @abstractmethod
    async def initialize_select(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def select(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def create_select_menu(
        self,
        ctx: Context,
        name: str,
        options: commands.Greedy[SelectOptionRoleConverter],
        min_values: Optional[int] = None,
        max_values: Optional[int] = None,
        *,
        placeholder: Optional[str] = None,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_select_menu(self, ctx: Context, *, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def options(self, ctx: Context) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def create_select_option(
        self,
        ctx: Context,
        name: str,
        role: RoleHierarchyConverter,
        label: Optional[str] = None,
        description: Optional[str] = None,
        emoji: Optional[Union[discord.PartialEmoji, str]] = None,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_select_option(self, ctx: Context, *, name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def send_select(
        self,
        ctx: Context,
        channel: discord.TextChannel,
        views: commands.Greedy[SelectRoleConverter],
        *,
        message: str,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def edit_with_select(
        self,
        ctx: Context,
        message: discord.Message,
        views: commands.Greedy[SelectRoleConverter],
    ) -> None:
        raise NotImplementedError()
