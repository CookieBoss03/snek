#!/usr/bin/env python3

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
                    fn(testcase_self, *entry)

        return spoof_test_fn

    return decorator


class MockInterface:
    def __init__(self):
        self.actions = []

    def send(self, *args):
        self.actions.append(("send", *args))

    def log(self, *args):
        pass  # Don't want to test logs

    def die(self):
        self.actions.append(("die"))


BEHAVIOR_TESTS = [
    [],
    [
        [["motd", "ohai"], ["join", TEST_USERNAME, TEST_PASSWORD]],
    ],
]

class BehaviorTests:
    def test_import(self):
        import secret
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
