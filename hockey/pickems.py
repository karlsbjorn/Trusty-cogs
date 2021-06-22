from __future__ import annotations
import logging
import discord
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

from redbot.core.i18n import Translator

from .constants import TEAMS
from .errors import NotAValidTeamError, UserHasVotedError, VotingHasEndedError
from .game import Game

_ = Translator("Hockey", __file__)
log = logging.getLogger("red.trusty-cogs.Hockey")


class PickemsButton(discord.ui.Button):
    def __init__(self, label: str, emoji: str, disabled: bool, custom_id: str):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=label,
            emoji=emoji,
            disabled=disabled,
            custom_id=custom_id,
        )
        self.disabled = disabled

    async def callback(self, interaction: discord.Interaction):
        time_now = datetime.utcnow()

        if str(interaction.user.id) in self.view.votes:
            if time_now > self.view.game_start:
                await interaction.response.send_message(
                    _("Voting has ended! You have voted for {emoji} {team}").format(
                        emoji=self.emoji, team=self.view.votes[str(interaction.user.id)]
                    ),
                    ephemeral=True,
                )
                self.view.disable_buttons()
                await interaction.message.edit(view=self.view)
                return
            if self.view.votes[str(interaction.user.id)] != self.label:
                self.view.votes[str(interaction.user.id)] = self.label
                await interaction.response.send_message(
                    _("You have already voted! Changing vote to: {emoji} {team}").format(
                        emoji=self.emoji, team=self.label
                    ),
                    ephemeral=True,
                )
                self.view._should_save = True
            else:
                await interaction.response.send_message(
                    _("You have already voted for {emoji} {team}!").format(
                        emoji=self.emoji, team=self.label
                    ),
                    ephemeral=True,
                )
        else:
            if time_now > self.view.game_start:
                await interaction.response.send_message(
                    _("Voting has ended! You did not vote on this game!"),
                    ephemeral=True,
                )
                return
            self.view.votes[str(interaction.user.id)] = self.label
            await interaction.response.send_message(
                _("Setting your vote to: {emoji} {team}").format(
                    emoji=self.emoji, team=self.label
                ),
                ephemeral=True,
            )
            self.view._should_save = True


class Pickems(discord.ui.View):
    """
    Pickems object for handling votes on games for the day
    """

    game_id: int
    game_state: str
    messages: List[str]
    guild: int
    game_start: datetime
    home_team: str
    away_team: str
    votes: dict
    name: str
    winner: str
    link: str
    _should_save: bool

    def __init__(self, **kwargs):
        super().__init__()
        self.game_id = kwargs.get("game_id")
        self.game_state = kwargs.get("game_state")
        self.messages = kwargs.get("messages", [])
        self.guild = kwargs.get("guild")
        self.game_start = kwargs.get("game_start")
        self.home_team = kwargs.get("home_team")
        self.away_team = kwargs.get("away_team")
        self.votes = kwargs.get("votes")
        self.home_emoji = (
            discord.PartialEmoji.from_str(TEAMS[self.home_team]["emoji"])
            if self.home_team in TEAMS
            else "\N{HOUSE BUILDING}\N{VARIATION SELECTOR-16}"
        )
        self.away_emoji = (
            discord.PartialEmoji.from_str(TEAMS[self.away_team]["emoji"])
            if self.away_team in TEAMS
            else "\N{AIRPLANE}\N{VARIATION SELECTOR-16}"
        )
        self.winner = kwargs.get("winner")
        self.name = kwargs.get("name")
        self.link = kwargs.get("link")
        self._should_save: bool = True
        # Start true so we save instantiated pickems
        self.game_type: str = kwargs.get("game_type")
        super().__init__(timeout=None)
        disabled_buttons = datetime.utcnow() > self.game_start
        self.home_button = PickemsButton(
            label=self.home_team,
            emoji=self.home_emoji,
            disabled=disabled_buttons,
            custom_id=f"home-{self.game_id}-{self.name}",
        )
        self.away_button = PickemsButton(
            label=self.away_team,
            emoji=self.away_emoji,
            disabled=disabled_buttons,
            custom_id=f"away-{self.game_id}-{self.name}",
        )
        self.add_item(self.home_button)
        self.add_item(self.away_button)

    def __repr__(self):
        return (
            "<Pickems game_id={0.game_id} game_state={0.game_state} "
            "game_type={0.game_type} name={0.name} guild={0.guild} winner={0.winner}>"
        ).format(self)

    def disable_buttons(self):
        self.home_button.disabled = True
        self.away_button.disabled = True

    def compare_game(self, game: Game) -> bool:
        return (
            self.home_team == game.home_team
            and self.away_team == game.away_team
            and self.game_start == game.game_start
        )

    def add_vote(self, user_id: int, team: discord.Emoji) -> None:
        time_now = datetime.utcnow()

        team_choice = None
        if str(team.id) in self.home_emoji:
            team_choice = self.home_team
        if str(team.id) in self.away_emoji:
            team_choice = self.away_team
        if team_choice is None:
            raise NotAValidTeamError()
        if str(user_id) in self.votes:
            choice = self.votes[str(user_id)]
            if time_now > self.game_start:
                if choice == self.home_team:
                    emoji = self.home_emoji
                if choice == self.away_team:
                    emoji = self.away_emoji
                raise VotingHasEndedError(_("You have voted for ") + f"<:{emoji}>")
            else:
                if choice != team_choice:
                    self.votes[str(user_id)] = team_choice
                    self._should_save = True
                    raise UserHasVotedError("{} {}".format(team, team_choice))
        if time_now > self.game_start:
            raise VotingHasEndedError(_("You did not vote on this game!"))
        if str(user_id) not in self.votes:
            self.votes[str(user_id)] = team_choice
            self._should_save = True

    def to_json(self) -> dict:
        return {
            "game_id": self.game_id,
            "game_state": self.game_state,
            "messages": self.messages,
            "guild": self.guild,
            "game_start": self.game_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "home_team": self.home_team,
            "away_team": self.away_team,
            "votes": self.votes,
            "name": self.name,
            "winner": self.winner,
            "link": self.link,
            "game_type": self.game_type,
        }

    @classmethod
    def from_json(cls, data: dict) -> Pickems:
        # log.debug(data)
        return cls(
            game_id=data.get("game_id"),
            game_state=data.get("game_state"),
            messages=data.get("messages", []),
            guild=data.get("guild"),
            game_start=datetime.strptime(data["game_start"], "%Y-%m-%dT%H:%M:%SZ"),
            home_team=data["home_team"],
            away_team=data["away_team"],
            votes=data["votes"],
            name=data.get("name", ""),
            winner=data.get("winner", None),
            link=data.get("link", None),
            game_type=data.get("game_type", "R"),
        )

    async def set_pickem_winner(self, game: Game) -> bool:
        """
        Sets the pickem object winner from game object

        Returns
        -------
        `True` if the winner has been set or the game is postponed
        `False` if the winner has not set and it's not time to clear it yet.
        """
        log.debug("Setting winner for %s", repr(self))
        if not game:
            return False
        if game.game_state == "Postponed":
            if game.game_start != self.game_start:
                self.game_start = game.game_start
                self._should_save = True
            return False
        if game.home_score > game.away_score:
            self.winner = self.home_team
            self._should_save = True
            return True
        elif game.away_score > game.home_score:
            self.winner = self.away_team
            self._should_save = True
            return True
        return False

    async def get_game(self) -> Game:
        return await Game.from_url(self.link)

    async def check_winner(self, game: Optional[Game] = None) -> bool:
        """
        allow the pickems objects to check winner on their own

        wrapper around set_pickems_winner method to pull the game object
        and return true or false depending on the state of the game

        This realistically only gets called once all the games are done playing
        """
        after_game = datetime.utcnow() >= (self.game_start + timedelta(hours=2))
        if self.winner:
            return True
        if game is not None:
            return await self.set_pickem_winner(game)
        if self.link and after_game:
            log.debug("Checking winner for %s", repr(self))
            game = await Game.from_url(self.link)
            return await self.set_pickem_winner(game)
        return False
