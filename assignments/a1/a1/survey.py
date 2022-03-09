"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin

=== Module Description ===

This file contains classes that describe a survey as well as classes that
described different types of questions that can be asked in a given survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, List
from criterion import HomogeneousCriterion, InvalidAnswerError

if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """ An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """ Initialize a question with the text <text> """
        # TODO: complete the body of this method
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """
        Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """ Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    # TODO: make this a child class of another class defined in this file
    """ A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string

    === Private Attributes ===
    _option: the answer allow you to choice
    """

    id: int
    text: str
    _option: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        """
        Initialize a question with the text <text> and id <id> and
        possible answers <options>.

        === Precondition ===
        No two elements in <options> are the same string
        <options> contains at least two elements
        """
        # TODO: complete the body of this method
        Question.__init__(self, id_, text)
        self._option = options

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        return "Question：{name}, Options{url}".format \
            (name=self.text, url=self._option)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the possible answers to this
        question.
        """
        # TODO: complete the body of this method
        return answer.content in self._option

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question.
        """
        # TODO: complete the body of this method
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class NumericQuestion(Question):
    # TODO: make this a child class of another class defined in this file
    """ A question whose answer can be an integer between some
    minimum and maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _maxi: the max integer that answer can be
    _minn: the min integer that answer can be

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    _maxi: int
    _minn: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """
        Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        === Precondition ===
        min_ < max_
        """
        # TODO: complete the body of this method
        Question.__init__(self, id_, text)
        self._minn = min_
        self._maxi = max_

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        return "Question：{name}, The integer must between {url} and {ww}\
        (inclusive)".format(name=self.text, url=self._minn, ww=self._maxi)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        # TODO: complete the body of this method
        if isinstance(answer.content, int):
            return self._minn <= int(answer.content) <= self._maxi
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity calculated by:

        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximimum
           and minimum possible answers.
        3. subtract the value from step 2 from 1.0

        Hint: this is the same calculation from the worksheet in lecture!

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        # TODO: complete the body of this method
        if answer1.content == answer2.content:
            return 1.0
        else:
            value2 = abs(answer2.content - answer1.content)
            value1 = self._maxi - self._minn
        return 1 * (1 - value2 / value1)


class YesNoQuestion(Question):
    # TODO: make this a child class of another class defined in this file
    """ A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """
        Initialize a question with the text <text> and id <id>.
        """
        # TODO: complete the body of this method
        Question.__init__(self, id_, text)

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        return "Question：{name}, Yes or No".format(name=self.text)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer>'s content is a boolean.
        """
        # TODO: complete the body of this method
        return isinstance(answer.content, bool)

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content is equal to <answer2>.content and
        return 0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        # TODO: complete the body of this method
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class CheckboxQuestion(Question):
    # TODO: make this a child class of another class defined in this file
    """ A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _option: the possible answer you can write

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    _option: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        """
        Initialize a question with the text <text> and id <id> and
        possible answers <options>.

        === Precondition ===
        No two elements in <options> are the same string
        <options> contains at least two elements
        """
        Question.__init__(self, id_, text)
        self._option = options

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        return "Question：{name}".format(name=self.text)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid iff its content is a non-empty list containing
        unique possible answers to this question.
        """
        # TODO: complete the body of this method
        lis = []
        if isinstance(answer.content, list) and len(answer.content) != 0:
            for ans in answer.content:
                if ans not in lis and ans in self._option:
                    lis.append(ans)
                else:
                    return False
            return True
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer1>.content == ['c', 'b', 'd'], the strings that are common to
        both are ['c', 'b'] and the unique strings that appear in both are
        ['a', 'b', 'c', 'd'].

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        # TODO: complete the body of this method
        appear = 0
        lis = []
        for ans in range(len(answer1.content)):
            if answer1.content[ans] in answer2.content:
                appear += 1
            if answer1.content[ans] not in lis:
                lis.append(answer1.content[ans])
        for i in range(len(answer2.content)):
            if answer2.content[i] not in lis:
                lis.append(answer2.content[i])
        return appear / len(lis)


class Answer:
    """ An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, List[str]]

    def __init__(self,
                 content: Union[str, bool, int, List[Union[str]]]) -> None:
        """Initialize an answer with content <content>"""
        # TODO: complete the body of this method
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff self.content is a valid answer to <question>"""
        # TODO: complete the body of this method
        return question.validate_answer(self)


class Survey:
    """
    A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping each question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight; an integer
              representing the importance of this criteria.
    _default_criterion: a criterion to use to evaluate a question if the
              question does not have an associated criterion in _criteria
    _default_weight: a weight to use to evaluate a question if the
              question does not have an associated weight in _weights

    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    Each key in _criteria occurs as a key in _questions
    Each key in _weights occurs as a key in _questions
    Each value in _weights is greater than 0
    _default_weight > 0
    """

    _questions: Dict[int, Question]
    _criteria: Dict[int, Criterion]
    _weights: Dict[int, int]
    _default_criterion: Criterion
    _default_weight: int

    def __init__(self, questions: List[Question]) -> None:
        """
        Initialize a new survey that contains every question in <questions>.
        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        # TODO: complete the body of this method
        self._questions = {}
        self._criteria = {}
        self._weights = {}
        for i in questions:
            if i.id not in self._questions:
                self._questions[i.id] = i
        self._default_criterion = HomogeneousCriterion()
        self._default_weight = 1

    def __len__(self) -> int:
        """ Return the number of questions in this survey """
        # TODO: complete the body of this method
        acc = 0
        for _ in self._questions:
            acc += 1
        return acc

    def __contains__(self, question: Question) -> bool:
        """
        Return True iff there is a question in this survey with the same
        id as <question>.
        """
        # TODO: complete the body of this method
        for i in self._questions:
            if i == question.id:
                return True
        return False

    def __str__(self) -> str:
        """
        Return a string containing the string representation of all
        questions in this survey

        You can choose the precise format of this string.
        """
        # TODO: complete the body of this method
        s = ''
        for i in self._questions:
            s += str(self._questions[i]) + ','
        return s

    def get_questions(self) -> List[Question]:
        """ Return a list of all questions in this survey """
        # TODO: complete the body of this method
        s = []
        for i in self._questions:
            s.append(self._questions[i])
        return s

    def _get_criterion(self, question: Question) -> Criterion:
        """
        Return the criterion associated with <question> in this survey.

        Iff <question>.id does not appear in self._criteria, return the default
        criterion for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        # TODO: complete the body of this method
        if question.id not in self._criteria:
            return self._default_criterion
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """
        Return the weight associated with <question> in this survey.

        Iff <question>.id does not appear in self._weights, return the default
        weight for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        # TODO: complete the body of this method
        if question.id not in self._weights:
            return self._default_weight
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """
        Set the weight associated with <question> to <weight> and return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        # TODO: complete the body of this method
        if question.id not in self._questions:
            return False
        else:
            self._weights[question.id] = weight
            return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """
        Set the criterion associated with <question> to <criterion> and return
        True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        # TODO: complete the body of this method
        if question.id not in self._questions:
            return False
        else:
            self._criteria[question.id] = criterion
            return True

    def score_students(self, students: List[Student]) -> float:
        """
        Return a quality score for <students> calculated based on their answers
        to the questions in this survey, and the associated criterion and weight
        for each question .

        This score is determined using the following algorithm:

        1. For each question in <self>, find its associated criterion, weight,
           and <students> answers to this question. Use the score_answers method
           for this criterion to calculate a quality score. Multiply this
           quality score by the associated weight.
        2. Find the average of all quality scores from step 1.

        If an InvalidAnswerError would be raised by calling this method, or if
        there are no questions in <self>, this method should return zero.

        === Precondition ===
        All students in <students> have an answer to all questions in this
            survey
        """
        # TODO: complete the body of this method
        if len(self.get_questions()) == 0:
            return 0
        res = []
        for i in self._questions:
            ans = []
            for x in students:
                ans.append(x.get_answer(self._questions[i]))
            try:
                score = self._get_criterion(self._questions[i]). \
                    score_answers(self._questions[i], ans)
            except InvalidAnswerError:
                return 0
            res.append(score * self._get_weight(self._questions[i]))
        return sum(res) / len(res)

    def score_grouping(self, grouping: Grouping) -> float:
        """ Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> this score is 0.0. Otherwise, this
        score is determined using the following algorithm:

        1. For each group in <grouping>, get the score for the members of this
           group calculated based on their answers to the questions in this
           survey.
        2. Return the average of all the scores calculated in step 1.

        === Precondition ===
        All students in the groups in <grouping> have an answer to all questions
            in this survey
        """
        # TODO: complete the body of this method
        if len(grouping.get_groups()) == 0:
            return 0
        gp = grouping.get_groups()
        res = []
        for i in gp:
            res.append(self.score_students(i.get_members()))
        return sum(res) / len(res)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper']})
