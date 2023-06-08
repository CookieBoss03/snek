#!/usr/bin/env python3

import logic
import unittest

TEST_USERNAME = "LOL"
TEST_PASSWORD = "YOLO"


# Disgusting bit of python dark magic that badly emulates parameterized tests.
# Note that the output is terrible, and all output is always seen.
def with_battery(test_battery):
    def decorator(fn):
        def spoof_test_fn(testcase_self):
            for i, entry in enumerate(test_battery):
                with testcase_self.subTest(i=i, entry=entry):
                    fn(testcase_self, entry)

        return spoof_test_fn

    return decorator


class MockInterface(logic.CallbackInterface):
    def __init__(self):
        self.actions = []

    def send(self, *args):
        self.actions.append(("send", *args))

    def log(self, *args):
        pass  # Don't want to test logs

    def die(self):
        self.actions.append(("die"))


BEHAVIOR_TESTS = [
    # Does this even work?
    [],
    # Does starting even work?
    [
        [
            ["motd", "ohai"],
            [
                ("send", "join", TEST_USERNAME, TEST_PASSWORD),
                ("send", "chat", "ohai"),
            ],
        ],
    ],
    # Do we die after an error?
    [
        [
            ["error", "505 or something"],
            [
                ("die"),
            ],
        ],
    ],
    # Do we crash after a chat message?
    [
        [
            ["chat", "42", "henlo"],
            [
            ],
        ],
    ],
    [
        [
            ["motd", "ohai"],
            [
                ("send", "join", TEST_USERNAME, TEST_PASSWORD),
                ("send", "chat", "ohai"),
            ],
        ],
        [
            ["chat", "42", "henlo"],
            [
            ],
        ],
    ],
]

class BehaviorTests(unittest.TestCase):
    def test_import_secret(self):
        import secret
        # Just to make sure it's properly formatted

    def test_import_bwbot(self):
        import bwbot
        # Just to make sure it's properly formatted

    @with_battery(BEHAVIOR_TESTS)
    def test_behavior(self, steps):
        mock_interface = MockInterface()
        game = logic.Logic(TEST_USERNAME, TEST_PASSWORD, mock_interface)
        for step_input, step_expected_outputs in steps:
            game.digest(step_input[0], step_input[1:])
            self.assertEqual(mock_interface.actions, step_expected_outputs)
            mock_interface.actions = []


if __name__ == "__main__":
    unittest.main()
