import unittest

from rename import multi_replace_curry


class TestFindLabel(unittest.TestCase):
    def setUp(self):
        pass

    def test_multi_replace_whenNoReplacements_returnSameName(self):
        name = "zhou"
        replacements = []

        self.assertEqual(name, multi_replace_curry(replacements)(name))

    def test_multi_replace_whenOneReplacements(self):
        name = "obama"
        replacements = [("obama", "trump")]

        self.assertEqual("trump", multi_replace_curry(replacements)(name))

    def test_multi_replace_whenTwoReplacements(self):
        name = "obama orange"
        replacements = [("obama", "trump"), ("banana", "apple")]

        self.assertEqual("trump orange", multi_replace_curry(replacements)(name))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
