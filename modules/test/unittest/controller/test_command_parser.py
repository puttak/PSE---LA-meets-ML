from typing import Dict

import pytest

from modules.controller.command_parser import CommandParser
from modules.controller.commands.classify_command import ClassifyCommand
from modules.controller.commands.collect_command import CollectCommand
from modules.controller.commands.command import Command
from modules.controller.commands.key import Key
from modules.controller.commands.label_command import LabelCommand
from modules.controller.commands.module import Module
from modules.controller.commands.train_command import TrainCommand
from modules.exception.exceptions import IllegalArgumentException
from modules.shared.configurations import Configurations
from mock import patch, call


def dicts_equal(actual: Dict[Key, str], expected: Dict[Key, str]) -> bool:
    for key, value in actual.items():
        if value is not None and key not in expected:
            return False
    for key, value in expected.items():
        if value != actual.get(key):
            return False
    return True


def test_valid_input_returns_command():
    input_string: str = "collect --name name --amount amount -p path --size size"
    expected = {
        Key.NAME: "name",
        Key.AMOUNT: "amount",
        Key.PATH: "path",
        Key.SIZE: "size"
    }
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, CollectCommand)
    assert dicts_equal(command.arguments, expected) is True


def test_valid_input_with_arguments():
    input_string: str = "train -p path -n name -t train -s savingPath"
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, TrainCommand)
    expected: Dict[Key, str] = {
        Key.PATH: "path",
        Key.NAME: "name",
        Key.TRAIN: "train",
        Key.SAVING_PATH: "savingPath"
    }
    assert dicts_equal(command.arguments, expected) is True


def test_valid_input_with_flag():
    input_string: str = "classify -p path -n network"
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, ClassifyCommand)
    expected: Dict[Key, str] = {
        Key.PATH: "path",
        Key.NETWORK: "network"
    }
    assert dicts_equal(command.arguments, expected) is True


def test_valid_collector_input():
    input_string: str = "collect --amount amount -n name -s size -p path"
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, CollectCommand)
    expected: Dict[Key, str] = {
        Key.AMOUNT: "amount",
        Key.NAME: "name",
        Key.SIZE: "size",
        Key.PATH: "path"
    }
    assert dicts_equal(command.arguments, expected) is True


def test_valid_label_mode():
    input_string = "label -n name --path path -s saving_path"
    expected = {
        Key.NAME: "name",
        Key.PATH: "path",
        Key.SAVING_PATH: "saving_path",
    }
    command = CommandParser.parse_input(input_string)
    assert isinstance(command, LabelCommand)
    assert dicts_equal(command.arguments, expected) is True


def test_fails_when_entering_invalid_module():
    input_string = "generate -s size -a amount"
    with pytest.raises(IllegalArgumentException):
        CommandParser.parse_input(input_string)


def test_quit_with_arguments_throws_error():
    input_string = "quit -n name --density density"
    with pytest.raises(IllegalArgumentException):
        CommandParser.parse_input(input_string)


def test_collector_with_missing_optional_args_adds_default():
    input_string = "collect -n name"
    size = Configurations.get_config_with_key(Module.COLLECT, Key.SIZE)
    amount = Configurations.get_config_with_key(Module.COLLECT, Key.AMOUNT)
    path = Configurations.get_config_with_key(Module.COLLECT, Key.PATH)
    expected = {
        Key.NAME: "name",
        Key.SIZE: size,
        Key.AMOUNT: amount,
        Key.PATH: path
    }
    command = CommandParser.parse_input(input_string)
    assert isinstance(command, CollectCommand)
    assert dicts_equal(command.arguments, expected) is True


def test_classify_command_with_missing_optional_arg_adds_default():
    input_str = "train -p path -n network"
    train = Configurations.get_config_with_key(Module.TRAIN, Key.TRAIN)
    saving_path = Configurations.get_config_with_key(Module.TRAIN, Key.SAVING_PATH)
    expected = {
        Key.PATH: "path",
        Key.NAME: "network",
        Key.TRAIN: train,
        Key.SAVING_PATH: saving_path,
        Key.NETWORK: None,
    }
    command = CommandParser.parse_input(input_str)
    assert isinstance(command, TrainCommand)
    assert dicts_equal(command.arguments, expected) is True


def test_input_calls_with_two_spaces():
    input_str = "label  -n name -p path -s saving_path"
    expected = {
        Key.PATH: "path",
        Key.NAME: "name",
        Key.SAVING_PATH: "saving_path",
    }
    command = CommandParser.parse_input(input_str)
    assert isinstance(command, LabelCommand)
    assert dicts_equal(command.arguments, expected) is True


@patch("modules.view.command_line_interface.CommandLineInterface")
def test_input_is_empty(mocked_cli):
    with pytest.raises(IllegalArgumentException):
        input_str = ""
        CommandParser.parse_input(input_str)
        mocked_cli.has_calls("IllegalArgumentException: Please enter the module you want to execute")
