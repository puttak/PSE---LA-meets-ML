from typing import Dict

import pytest

from modules.controller.command_parser import CommandParser
from modules.controller.commands.classify_command import ClassifyCommand
from modules.controller.commands.collect_command import CollectCommand
from modules.controller.commands.command import Command
from modules.controller.commands.key import Key
from modules.controller.commands.label_command import LabelCommand
from modules.controller.commands.label_mode import LabelMode
from modules.controller.commands.train_command import TrainCommand
from modules.exception.excpetions import IllegalArgumentException


def test_valid_input_returns_command():
    input_string: str = "collect --name name --density density --amount amount -p path --size size"
    expected = {
        Key.NAME: "name",
        Key.DENSITY: "density",
        Key.AMOUNT: "amount",
        Key.PATH: "path",
        Key.SIZE: "size"
    }
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, CollectCommand)
    assert command.arguments == expected


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
    assert command.arguments == expected


def test_valid_input_with_flag():
    input_string: str = "classify -p path -s -n network"
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, ClassifyCommand)
    expected: Dict[Key, str] = {
        Key.PATH: "path",
        Key.SOLVE: "",
        Key.NETWORK: "network"
    }
    assert command.arguments == expected


def test_invalid_mode_throws_exception():
    input_string: str = "label -n name -p path"
    with pytest.raises(IllegalArgumentException):
        CommandParser.parse_input(input_string)


def test_valid_collector_input():
    input_string: str = "collect --amount amount -n name -s size --density density -p path"
    command: Command = CommandParser.parse_input(input_string)
    assert isinstance(command, CollectCommand)
    expected: Dict[Key, str] = {
        Key.AMOUNT: "amount",
        Key.NAME: "name",
        Key.SIZE: "size",
        Key.DENSITY: "density",
        Key.PATH: "path"
    }
    assert command.arguments == expected


def test_valid_label_label_mode():
    input_string = "label label -n name --path path -s saving_path"
    expected = {
        Key.NAME: "name",
        Key.PATH: "path",
        Key.SAVING_PATH: "saving_path",
    }
    command = CommandParser.parse_input(input_string)
    assert isinstance(command, LabelCommand)
    assert command._mode == LabelMode.LABEL
    assert command.arguments == expected


def test_valid_label_add_mode():
    input_string = "label add algo1 algo2 algo3"
    expected = [
        "algo1",
        "algo2",
        "algo3",
    ]
    command = CommandParser.parse_input(input_string)
    assert isinstance(command, LabelCommand)
    assert command._mode == LabelMode.ADD
    assert command._configs == expected


def test_valid_label_remove_mode():
    input_string = "label remove algo1"
    expected = ["algo1"]
    command = CommandParser.parse_input(input_string)
    assert isinstance(command, LabelCommand)
    assert command._mode == LabelMode.REMOVE
    assert command._configs == expected


def test_fails_when_entering_invalid_module():
    input_string = "generate -s size -a amount"
    with pytest.raises(IllegalArgumentException):
        CommandParser.parse_input(input_string)


def test_quit_with_arguments_throws_error():
    input_string = "quit -n name --density density"
    with pytest.raises(IllegalArgumentException):
        CommandParser.parse_input(input_string)
