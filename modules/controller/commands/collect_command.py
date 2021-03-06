from modules.controller.commands.command import Command
from modules.controller.commands.key import Key
from modules.controller.commands.module import Module
from modules.model.collector_module.collector import Collector


##  command to execute the collector module
#
#   this command class will be created when entering collect in the command line
#   @extends Command to use its parsing logic
class CollectCommand(Command):

    def __init__(self):
        super().__init__()
        self.module_name = Module.COLLECT
        self.valid_arguments = {
            ("a", "amount"): Key.AMOUNT,
            ("n", "name"): Key.NAME,
            ("p", "path"): Key.PATH,
            ("s", "size"): Key.SIZE,
            ("h", "help"): Key.HELP,
        }

        self.help_arguments = (
            "-a <amount> (optional) Absolute amount of matrices the user wants to generate [default: 100]",
            "-n <name> (optional) Name under which the matrices will be saved "
            "[default: \"unlabeled_matrix_\" + current date and time]",
            "-s <size> (optional) Absolute size the generated square matrices should have. [default: 128]",
            "-p <path> (optional) Path where the created/downloaded matrices will be saved "
            "[default: data/UnlabeledMatrices/]",
        )

        self.arguments = {
            Key.AMOUNT: None,
            Key.NAME: None,
            Key.PATH: None,
            Key.SIZE: None
        }

    def execute(self):
        super().execute()
        Collector.collect(
            amount=self.get_int_value(Key.AMOUNT),
            size=self.get_int_value(Key.SIZE),
            name=self.arguments.get(Key.NAME),
            path=self.arguments.get(Key.PATH),
        )
