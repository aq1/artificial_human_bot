from bot.commands import (
    BaseCommand,
    AdminPermissionMixin,
)


class PoloniexBalanceCommand(AdminPermissionMixin, BaseCommand):

    _COMMAND = 'poloniex_balance'

    @property
    def _success_message(self):
        return 'poloniex_balance'
