import datetime
from typing import List, Dict, Optional, Tuple
from modules.controller.commands.key import Key
from modules.controller.commands.module import Module
from modules.exception.exceptions import IllegalArgumentException
from modules.shared.configurations import Configurations


##  Interface for the module specific commands
class Command:

    def __init__(self):
        self.__module_name: Module = Module.UNDEFINED
        self.__arguments: Dict[Key, str] = {}
        self.__valid_arguments: Dict[Tuple[str, str], Key] = {}
        self.__help_arguments: Tuple[str] = ()

    @property
    def module_name(self) -> Module:
        return self.__module_name

    @module_name.setter
    def module_name(self, module: Module) -> None:
        self.__module_name = module

    @property
    def arguments(self) -> Dict[Key, str]:
        return self.__arguments

    @arguments.setter
    def arguments(self, arguments: Dict[Key, str]) -> None:
        self.__arguments = arguments

    @property
    def valid_arguments(self) -> Dict[Tuple[str, str], Key]:
        return self.__valid_arguments

    @valid_arguments.setter
    def valid_arguments(self, args: Dict[Tuple[str, str], Key]) -> None:
        self.__valid_arguments = args

    @property
    def help_arguments(self) -> Tuple[str]:
        return self.__help_arguments

    @help_arguments.setter
    def help_arguments(self, args: Tuple[str]) -> None:
        self.__help_arguments = args

    ##  can be called the execute the module
    def execute(self) -> None:
        pass

    def __add_default_args(self) -> None:
        for key, value in self.arguments.items():
            if value is None:
                self.__set_values(key)

    ##  parses the string list into a dict of args
    #
    #   @param args the list retrieved by the input
    def set_args(self, arg_list: List[str]) -> None:
        while len(arg_list) != 0:
            next_key = arg_list.pop(0)
            key: Key = self.__get_key(next_key)
            value: str = ""
            if len(arg_list) and not arg_list[0].startswith("-"):
                value = arg_list.pop(0)
            self.arguments[key] = value
        self.__add_default_args()

    def __get_key(self, next_key: str) -> Key:
        key: Key = None
        if next_key.startswith("--"):
            key = self.__get_arguments_key(next_key[2:])
        elif next_key.startswith("-"):
            key = self.__get_arguments_key(next_key[1:])
        if key is None:
            raise IllegalArgumentException("%s is not a valid argument." % next_key)
        return key

    def __get_arguments_key(self, tag: str) -> Key:
        for key, value in self.valid_arguments.items():
            if tag in key:
                return value

    ##  Gives you the integer value associated with that key
    #
    #   Example:
    #   '''
    #       arguments = {Key.AMOUNT: "100"}
    #       command.get_int_value(Key.AMOUNT)   //  returns 100 as integer
    #   '''
    #
    #   @param key which you want a integer value for
    #   @throws IllegalArgumentException when self.argument[key] is not a integer (e.g. 4, 3000, ...)
    def get_int_value(self, key: Key) -> Optional[int]:
        result: int = None
        if key in self.arguments:
            try:
                result = int(self.arguments.get(key))
            except ValueError:
                raise IllegalArgumentException(self.arguments.get(key) + " is not a integer")
        return result

    ##  Gives you the the float value associated with that key
    #
    #   Example:
    #   '''
    #       arguments = {Key.TRAIN: "0.8"}
    #       command.get_int_value(Key.TRAIN)   //  returns 0.8 as a float
    #   '''
    #
    #   @param key which you want a float value for
    #   @throws IllegalArgumentException when self.arguments[key] is not float (e.g. 0.6, 3, ...)
    def get_float_value(self, key: Key) -> Optional[float]:
        result: float = None
        if key in self.arguments:
            try:
                result = float(self.arguments.get(key))
            except ValueError:
                raise IllegalArgumentException(self.arguments.get(key) + " is not a float")
        return result

    def __set_values(self, key):
        if key is Key.NAME:
            standard_name = Configurations.get_config_with_key(self.module_name, key)
            current_dt = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
            self.arguments[key] = standard_name + current_dt
        else:
            self.arguments[key] = Configurations.get_config_with_key(self.module_name, key)
