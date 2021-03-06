from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from random import randint


doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust1'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'trust1/Instructions.html'
    point_template = 'trust1/Point.html'

    # Initial amount allocated to each player

    # 初期持ちポイント
    endowment = c(1000)
    # 何倍にして返すか
    multiplier = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # プレイヤー１が送る
    sent_amount = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""Amount sent by P1""",
    )

    # プレイヤー２が送る
    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P1""",
        min=c(0),
    )

    # CPUが送る
    sent_cpu = models.IntegerField(initial=randint(0, 1000))

    # CPUが送り返す
    def sent_back_cpu(self):
        return randint(0, self.sent_amount * 3)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        # Y(a)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_cpu() * Constants.multiplier
        # X(a)
        p2.payoff = self.sent_amount * Constants.multiplier - self.sent_back_cpu()

    def count1(self):
        return Constants.endowment - self.sent_amount

    def xb(self):
        return self.sent_cpu * Constants.multiplier - self.sent_back_amount

    def yb(self):
        return Constants.endowment - self.sent_cpu + self.sent_back_amount * Constants.multiplier


class Player(BasePlayer):

    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]
