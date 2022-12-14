import algorithms
from grammar import Grammar as Gr
import unittest


class TestIsLanguageEmpty(unittest.TestCase):
    def test_classic(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"E+T", "T"},
                         "T": {"T*F", "F"},
                         "F": {"(E)", "a"},
                     },
                     "E")  # Аксиома
        expected_answer = False
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_classic_missing_rule(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"E+T", "T"},
                         "F": {"(E)", "a"},
                     },
                     "E")  # Аксиома
        expected_answer = True
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_no_rules(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     dict(),  # Правила вывода
                     "E")  # Аксиома
        expected_answer = True
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_immediate_terminal(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"a"},
                     },
                     "E")  # Аксиома
        expected_answer = False
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_cycle(self):
        input_g = Gr({"A", "B", "C"},  # Нетерминалы
                     set(),  # Терминалы
                     {  # Правила вывода
                         "A": {"B"},
                         "B": {"C"},
                         "C": {"A"},
                     },
                     "A")  # Аксиома
        expected_answer = True
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_repeating_chars(self):
        input_g = Gr({"A", "B", "C"},  # Нетерминалы
                     {"a", "b", "c"},  # Терминалы
                     {  # Правила вывода
                         "A": {"BaaB"},
                         "B": {"CcCcC"},
                         "C": {"ccc"},
                     },
                     "A")  # Аксиома
        expected_answer = False
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )

    def test_many_nonterminals(self):
        input_g = Gr({"A", "B", "C", "O"},  # Нетерминалы
                     {"a", "b", "c", "o"},  # Терминалы
                     {  # Правила вывода
                         "A": {"ABOBA", "ABBA", "B"},
                         "B": {"CoCa", "Bb"},
                         "C": {"ccc"},
                         "O": {"abOba", "A"}
                     },
                     "A")  # Аксиома
        expected_answer = False
        self.assertEqual(
            algorithms.isLanguageEmpty(input_g)[0],
            expected_answer
        )


class TestUnreachableSymbols(unittest.TestCase):
    def test_classic(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"E+T", "T"},
                         "T": {"T*F", "F"},
                         "F": {"(E)", "a"},
                     },
                     "E")  # Аксиома
        expected_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"E+T", "T"},
                         "T": {"T*F", "F"},
                         "F": {"(E)", "a"},
                     },
                     "E")  # Аксиома

        self.assertEqual(
            algorithms.unreachableSymbols(input_g),
            expected_g
        )
        self.assertEqual(
            algorithms.unreachableSymbolsShort(input_g),
            expected_g
        )

    def test_classic_missing_rule(self):
        input_g = Gr({"E", "T", "F"},  # Нетерминалы
                     {"a", "+", "*", "(", ")"},  # Терминалы
                     {  # Правила вывода
                         "E": {"E+T", "T"},
                         "F": {"(E)", "a"},
                     },
                     "E")  # Аксиома
        expected_g = Gr({"E", "T"},  # Нетерминалы
                        {"+"},  # Терминалы
                        {  # Правила вывода
                            "E": {"E+T", "T"},
                        },
                        "E")  # Аксиома
        self.assertEqual(
            algorithms.unreachableSymbols(input_g),
            expected_g
        )
        self.assertEqual(
            algorithms.unreachableSymbolsShort(input_g),
            expected_g
        )

class TestExcessLambdaRules(unittest.TestCase):
    def test_classic1(self):
        input_g = Gr(
            {'A', 'B', 'M', 'N', 'K', 'S'},
            {'a', 'b'},
            {  # Правила вывода
                'A': {''},
                'B': {''},
                'M': {'AB'},
                'N': {'Ab'},
                'K': {'ab'},
                'S': {'KNM'}
            },
            'S'
        )
        expected_g = Gr(
            {'N', 'K', 'S'},
            {'a', 'b'},
            {  # Правила вывода
                'N': {'b'},
                'K': {'ab'},
                'S': {'KN'},
            },
            'S'
        )

        self.assertEqual(
            algorithms.wipeExcessLambdaRules(input_g),
            expected_g
        )

    def test_classic2(self):
        input_g = Gr(
            {'A', 'B', 'M', 'N', 'K', 'S'},
            {'a', 'b', 'c', 'p'},
            {  # Правила вывода
                'A': {'', 'c'},
                'B': {'', 'p'},
                'M': {'AB'},
                'N': {'Ab'},
                'K': {'ab'},
                'S': {'KNM'},
            },
            'S'
        )
        expected_g = Gr(
            {'A', 'B', 'M', 'N', 'K', 'S'},
            {'a', 'b', 'c', 'p'},
            {  # Правила вывода
                'A': {'c'},
                'B': {'p'},
                'M': {'AB', 'A', 'B'},
                'N': {'Ab', 'b'},
                'K': {'ab'},
                'S': {'KNM', 'KN'},
            },
            'S'
        )

        self.assertEqual(
            algorithms.wipeExcessLambdaRules(input_g),
            expected_g
        )
    
    def test_classic3(self):
        input_g = Gr(
            {'S'},
            {'a', 'b'},
            {  # Правила вывода
                'S': {'aSbS', 'bSaS', ''}
            },
            'S'
        )
        expected_g = Gr(
            {'S', 'new_S'},
            {'a', 'b'},
            {  # Правила вывода
                'S': {'aSbS', 'abS', 'aSb', 'ab', 'bSaS', 'bSa', 'baS', 'ba'},
                'new_S': {'', 'S'}
            },
            'new_S'
        )

        self.assertEqual(
            algorithms.wipeExcessLambdaRules(input_g),
            expected_g
        )


unittest.main()
