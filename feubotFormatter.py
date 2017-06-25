from discord.ext.commands import HelpFormatter

class FeubotFormatter(HelpFormatter):
    def filter_command_list(self):
        return sorted(super().filter_command_list(), key=lambda e: str.lower(e[0]))

