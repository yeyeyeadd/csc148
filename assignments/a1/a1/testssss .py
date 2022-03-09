from course import *
from course import *
from survey import *
from criterion import *
from grouper import *

import pytest
from typing import List, Set, FrozenSet
from example_usage import *
from hypothesis import given


class Test_Student:

    def test__str_(self) -> None:
        a = [2, anna]
        assert hasattr(n, a[1])

    def test_has_answer(self) -> None:
        a = [1, anna]
        q = [1, 'ok', 'o']

    def test_set_answer(self) -> None:
        a = []


class Test_MultipleChoiceQuestion(self):

    def test__str_(self) -> None:
        a = []
        a.append(
            "The text of the question is" + self.text + "and the possible answers are" + self.options)
        assert hasattr(question, a)

    def test_validate_answer(self) -> None:
        answer = []
        answer.append(1)
        options = []
        options.append(1, 2, 3)
        assert j.is_validate_answer

    def test_get_similarity(self) -> None:
        answer1 = [1, u]
        answer2 = [1, u]
        assert MultipleChoiceQuestion.test_get_similarity == 1.0


class Test_NumericQuestion(self):

    def test__str_(self) -> None:
        q = [
            "The text of the question is" + self.text + "and the possible answer is between" + self.min + "and" + \
            self.max]
        assert hasattr(self.text, q)

    def test_validate_answer(self) -> None:
        answer = 3
        min = 2
        max = 4
        assert answer.is_validate_answer is True

    def test_get_similarity(self) -> None:
        answer1 = 3
        answer2 = 2
        min = 1
        max = 4
        assert get_similarity(answer1, answer2) == 2


if __name__ == '__main__':
    pytest.main(['a1_pytest.py'])
