from course import *
from survey import *
from criterion import *
from grouper import *
import pytest
from example_usage import *


def test_sort_students() -> None:
    # initialize list
    students = [Student(1, 'c'), Student(2, 'b'), Student(3, 'd')]

    # test sort by id
    assert sort_students(students, 'id') == students

    # test sort by name
    alpha = sort_students(students, 'name')
    k = []
    for num in alpha:
        k.append(num.name)
    assert k == ['b', 'c', 'd']


def test_student_basic() -> None:
    # setup students
    s1 = Student(1, '1')
    s2 = Student(2, '2')

    # question
    q1 = Question(1, 'Q1')
    q2 = Question(2, 'Q2')

    # answer
    a1 = Answer("Answer for Q1")
    a2 = Answer("c")

    # Test __str__name
    assert str(s1) == s1.name
    assert str(s2) != s1.name

    # Test get answer None cases
    assert s1.get_answer(q1) is None

    # ----------------------------------------------------------
    # set answer + get asnwer

    # Test get answer + set answer
    s1.set_answer(q1, a1)
    assert s1.get_answer(q1) == a1

    # Test get answer + set answer(override)
    s1.set_answer(q1, a2)
    assert s1.get_answer(q1) == a2

    # Test get answer + set answer(None)
    assert s1.get_answer(q2) is None

    # ----------------------------------------------------
    # Test has_answer(no answer)
    assert s2.has_answer(q1) == False

    # Test has_answer
    m = MultipleChoiceQuestion(1, "MQ", ['a', 'b', 'c', 'd'])
    s1.set_answer(m, a2)
    assert s1.get_answer(q1) == a2
    assert s1.has_answer(m)

    # Test has_answer(Invalid answer)
    s1.set_answer(m, a1)
    assert s1.has_answer(m) == False


def test_course_basic() -> None:
    # set up course
    c1 = Course("CSC165")
    c2 = Course("CSC148")

    # set up student
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    s3 = Student(3, '3')
    s4 = Student(4, '4')
    s5 = Student(5, '5')
    s6 = Student(6, '6')

    # set up question
    q1 = Question(1, 'Q1')
    q2 = Question(2, 'Q2')
    m = MultipleChoiceQuestion(1, "MQ", ["A", "B", "C", "D"])
    n = NumericQuestion(2, "Numerical Question", 1, 10)

    # set up answer
    a1 = Answer("A1")
    a2 = Answer("A")

    # set up survey
    su1 = Survey([m])
    su2 = Survey([m, n])

    # test enroll_students
    c1.enroll_students([s2, s1])
    assert c1.students == [s2, s1]
    assert c1.students != [s1, s2]

    # test enroll_students(Duplicate)
    c1.enroll_students([s1, s2])
    assert c1.students == [s2, s1]

    # test get_students(None)
    assert c2.get_students() == ()

    # test get_students(Order)
    assert c1.get_students() == (s1, s2)

    # test all_answered(no student + no question)
    assert c2.all_answered(su1)
    assert c1.all_answered(Survey([]))

    # test all_answered(single question)

    # no valid answer
    s1.set_answer(m, a1)
    c2.enroll_students([s1])
    assert c2.all_answered(su1) == False
    # valid answer
    s1.set_answer(m, a2)
    assert c2.all_answered(su1) == True
    c2.enroll_students([s2])
    s2.set_answer(m, a2)
    assert c2.all_answered(su1) == True
    # two items, one with invalid answer
    s2.set_answer(m, a1)
    assert c2.all_answered(su1) == False

    # multiple questions
    c3 = Course("1")
    s6.set_answer(m, a2)
    c3.enroll_students([s6])
    assert c3.all_answered(su2) == False
    s6.set_answer(n, Answer(5))
    assert c3.all_answered(su2) == True


def test_mq_basic() -> None:
    # initialize
    options = ["a", "b", "c", "d"]
    m = MultipleChoiceQuestion(1, 'mq', options)
    a1 = Answer("A1")
    a2 = Answer("a")

    # test __str__()
    assert "mq" in str(m)
    for item in options:
        assert item in str(m)

    # test validate_answer
    assert m.validate_answer(a1) == False
    assert m.validate_answer(a2)

    # test get_similarity
    assert m.get_similarity(a2, a2) == 1.0
    assert m.get_similarity(a1, a2) == 0.0


def test_nq_basic() -> None:
    n = NumericQuestion(1, "nq", 1, 10)
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(-2)
    a2 = Answer(5)
    a3 = Answer(7)
    # test __str__()
    assert "nq" in str(n)
    assert str(1) in str(n) and str(10) in str(n)

    # test validate_answer
    assert n.validate_answer(a1) == False
    assert n.validate_answer(a2)

    # test get_similarity
    assert n.get_similarity(a2, a2) == 1.0
    assert n.get_similarity(a2, a3) == 1 - (2 / 9)


def test_yn_basic() -> None:
    y = YesNoQuestion(1, 'yn')
    s1 = Student(1, '1')
    s2 = Student(2, '2')
    a1 = Answer(True)
    a2 = Answer(1)
    a3 = Answer(False)
    # test __str__()
    assert "yn" in str(y)

    # test validate_answer
    assert y.validate_answer(a1)
    assert y.validate_answer(a2) == False

    # test get_similarity
    assert y.get_similarity(a2, a2) == 1.0
    assert y.get_similarity(a2, a3) == 0


def test_cq_basic() -> None:
    options = ['a', 'b', 'c', 'd']
    cq = CheckboxQuestion(1, "cq", options)
    a1 = Answer(['a'])
    a2 = Answer(1)
    a3 = Answer(False)
    # test __str__()
    assert "cq" in str(cq)

    # test validate_answer
    assert cq.validate_answer(a1)
    assert cq.validate_answer(a2) == False
    assert cq.validate_answer(Answer(['a', 'a'])) == False

    # test get_similarity
    assert cq.get_similarity(Answer(['a', 'a']), Answer(['b', 'b'])) == 0.0
    assert cq.get_similarity(Answer(['a', 'b']), Answer(['a', 'b'])) == 1.0
    assert cq.get_similarity(Answer(['d', 'e', 'c']),
                             Answer(['f', 'g', 'c'])) == 0.2


def test_answer_basic() -> None:
    options = ['a', 'b', 'c', 'd']
    m = MultipleChoiceQuestion(1, 'mq', options)
    a1 = Answer(1)
    a2 = Answer('a')
    a3 = Answer(['a'])
    a4 = Answer(True)
    assert a1.is_valid(m) == False
    assert a2.is_valid(m) == True
    assert a3.is_valid(m) == False
    assert a4.is_valid(m) == False

    cq = CheckboxQuestion(1, 'cq', options)
    assert a1.is_valid(cq) == False
    assert a2.is_valid(cq) == False
    assert a3.is_valid(cq) == True
    assert a4.is_valid(m) == False

    y = YesNoQuestion(1, 'yn')
    assert a1.is_valid(y) == False
    assert a2.is_valid(y) == False
    assert a3.is_valid(y) == False
    assert a4.is_valid(y) == True

    n = NumericQuestion(1, 'nq', 1, 10)
    assert a1.is_valid(n) == True
    assert a2.is_valid(n) == False
    assert a3.is_valid(n) == False
    assert a4.is_valid(n) == True


def test_homo_criterion() -> None:
    choice = ["a", "b", "c", "d"]
    option = ["A", "B", "C", "D"]
    num = [1, 2, 3, 4, 5, 6]
    bol = [True, False]

    c = HomogeneousCriterion()
    m = MultipleChoiceQuestion(1, 'mc', choice)
    n = NumericQuestion(2, 'nq', 1, 10)
    y = YesNoQuestion(3, "y")
    cq = CheckboxQuestion(4, 'cq', option)
    for item in choice:
        assert c.score_answers(m, [Answer(item)]) == 1.0
    for item in option:
        assert c.score_answers(cq, [Answer([item])]) == 1.0
    for item in bol:
        assert c.score_answers(y, [Answer(item)]) == 1.0
    for item in num:
        assert c.score_answers(n, [Answer(item)]) == 1.0

    with pytest.raises(InvalidAnswerError):
        assert c.score_answers(m, [Answer(True)])


def test_hete_criterion() -> None:
    choice = ["a", "b", "c", "d"]
    option = ["A", "B", "C", "D"]
    an = [Answer('a'), Answer('b'), Answer('c')]
    num = [1, 2, 3, 4, 5, 6]
    bol = [True, False]

    c = HeterogeneousCriterion()
    m = MultipleChoiceQuestion(1, 'mc', choice)
    n = NumericQuestion(2, 'nq', 1, 10)
    y = YesNoQuestion(3, "y")
    cq = CheckboxQuestion(4, 'cq', option)
    for item in choice:
        assert c.score_answers(m, [Answer(item)]) == 0.0
    for item in option:
        assert c.score_answers(cq, [Answer([item])]) == 0.0
    for item in bol:
        assert c.score_answers(y, [Answer(item)]) == 0.0
    for item in num:
        assert c.score_answers(n, [Answer(item)]) == 0.0

    assert c.score_answers(m, an) == 1.0
    with pytest.raises(InvalidAnswerError):
        assert c.score_answers(m, [Answer(True)])


def test_lone_criterion() -> None:
    choice = ["a", "b", "c", "d"]
    option = ["A", "B", "C", "D"]
    unique = [Answer('a'), Answer('a'), Answer('b')]
    notu = [Answer('a'), Answer('a'), Answer('a')]
    num = [1, 2, 3, 4, 5, 6]
    bol = [True, False]

    c = LonelyMemberCriterion()
    m = MultipleChoiceQuestion(1, 'mc', choice)
    n = NumericQuestion(2, 'nq', 1, 10)
    y = YesNoQuestion(3, "y")
    cq = CheckboxQuestion(4, 'cq', option)
    for item in choice:
        assert c.score_answers(m, [Answer(item)]) == 0.0
    for item in option:
        assert c.score_answers(cq, [Answer([item])]) == 0.0
    for item in bol:
        assert c.score_answers(y, [Answer(item)]) == 0.0
    for item in num:
        assert c.score_answers(n, [Answer(item)]) == 0.0
    assert c.score_answers(m, unique) == 0.0
    assert c.score_answers(m, notu) == 1.0

    with pytest.raises(InvalidAnswerError):
        assert c.score_answers(m, [Answer(True)])


def test_alpha_grouper() -> None:
    # Order-size 1
    grouper = AlphaGrouper(2)
    students = [Student(1, 'a'), Student(2, 'c'), Student(3, 'b'),
                Student(4, 'd')]
    course = Course('1')
    course.enroll_students(students)
    grouping = grouper.make_grouping(course, Survey([]))
    assert len(grouping) == 2
    k = []
    for item in grouping.get_groups():
        for s in item.get_members():
            k.append(s.name)
    assert k == ['a', 'b', 'c', 'd']

    # order-size2
    course = Course('2')
    grouper1 = AlphaGrouper(3)
    course.enroll_students(students[::-1])
    grouping = grouper1.make_grouping(course, Survey([]))
    assert len(grouping) == 2
    assert len(grouping.get_groups()[0]) == 3
    k = []
    for item in grouping.get_groups():
        for s in item.get_members():
            k.append(s.name)
    assert k == ['a', 'b', 'c', 'd']

    # Random order
    course = Course('3')
    grouper3 = AlphaGrouper(4)
    random.shuffle(students)
    course.enroll_students(students)
    grouping = grouper3.make_grouping(course, Survey([]))
    assert len(grouping) == 1
    assert len(grouping.get_groups()[0]) == 4
    k = []
    for item in grouping.get_groups():
        for s in item.get_members():
            k.append(s.name)
    assert k == ['a', 'b', 'c', 'd']


def test_random_grouper() -> None:
    grouper = RandomGrouper(2)
    students = [Student(1, 'a'), Student(2, 'c'), Student(3, 'b'),
                Student(4, 'd')]
    course = Course('1')
    course.enroll_students(students)
    grouping = grouper.make_grouping(course, Survey([]))
    assert len(grouping) == 2

    # order-size2
    course = Course('2')
    grouper1 = RandomGrouper(3)
    course.enroll_students(students[::-1])
    grouping = grouper1.make_grouping(course, Survey([]))
    assert len(grouping) == 2
    assert len(grouping.get_groups()[0]) == 3


def test_greedy_grouper() -> None:
    grouper = GreedyGrouper(2)
    course = Course('1')
    students = [Student(1, '1'), Student(2, '2'), Student(3, '3'),
                Student(4, '4')]
    q = YesNoQuestion(3, "Y")
    k = [True, False, False, False]
    for num in range(0, len(students)):
        students[num].set_answer(q, Answer(k[num]))
    course.enroll_students(students[::-1])
    su = Survey([q])
    grouping = grouper.make_grouping(course, su)
    assert len(grouping) == 2
    assert len(grouping.get_groups()[0]) == 2
    k = []
    for item in grouping.get_groups():
        for s in item.get_members():
            k.append(s.name)
    assert k == ['1', '2', '3', '4']


def test_window_grouper() -> None:
    grouper = WindowGrouper(2)
    course = Course('1')
    students = [Student(1, '1'), Student(2, '2'), Student(3, '3'),
                Student(4, '4')]
    q = YesNoQuestion(3, "Y")
    k = [True, False, False, False]
    for num in range(0, len(students)):
        students[num].set_answer(q, Answer(k[num]))
    course.enroll_students(students[::-1])
    su = Survey([q])
    grouping = grouper.make_grouping(course, su)
    assert len(grouping) == 2
    assert len(grouping.get_groups()[0]) == 2
    k = []
    for item in grouping.get_groups():
        for s in item.get_members():
            k.append(s.name)
    assert k == ['2', '3', '1', '4']


def test_sort_help() -> None:
    a = GreedyGrouper(2)
    students = [Student(1, '1'), Student(2, '2'), Student(3, '3')]
    s = Student(1, '1')
    max_ = s
    su = Survey([])
    assert a._sort_help(s, students, su, max_).name == '1'


def test_slice_list() -> None:
    lst = list(range(4))
    assert grouper.slice_list(lst, 2) == [[0, 1], [2, 3]]


def test_windows() -> None:
    lst = list(range(5))
    assert grouper.windows(lst, 4) == [[0, 1, 2, 3], [1, 2, 3, 4]]


class TestGroup:
    def test_init_attributes(self) -> None:
        """Test that the attributes have been initialized."""

    s1 = course.Student(1, 'Thomas'),
    s2 = course.Student(2, 'Fo'),
    s3 = course.Student(3, 'DD'),
    s4 = course.Student(4, 'DW')
    g = grouper.Group([s1, s2, s3, s4])
    assert g.members == [s1, s2, s3, s4]

    def test_len_group(self) -> None:
        """Group of length 4"""
        s1 = course.Student(1, 'Thomas'),
        s2 = course.Student(2, 'Fo'),
        s3 = course.Student(3, 'DD'),
        s4 = course.Student(4, 'DW')
        g = grouper.Group([s1, s2, s3, s4])
        length = len(g)
        assert length == 4

    def test_contains_true(self) -> None:
        """Member is in group."""
        s4 = course.Student(4, 'DW')
        g = grouper.Group([course.Student(1, 'Thomas'),
                           course.Student(2, 'Fo'),
                           course.Student(3, 'Dd'),
                           s4])
        bool_val = g.__contains__(s4)
        assert bool_val is True

    def test_str(self) -> None:
        g = grouper.Group([course.Student(1, 'Thomas'),
                           course.Student(2, 'Fo'),
                           course.Student(3, 'Dd'),
                           course.Student(4, 'DW')])
        group_members = str(g)
        assert group_members == 'Thomas,Fo,Dd,DW'

    def test_get_members(self) -> None:
        s1 = course.Student(1, 'Thomas'),
        s2 = course.Student(2, 'Fo'),
        s3 = course.Student(3, 'DD'),
        s4 = course.Student(4, 'DW')
        g = grouper.Group([s1, s2, s3, s4])
        people = g.get_members()
        assert people == [s1, s2, s3, s4]


class TestGrouping:

    def test_init_attributes(self) -> None:
        grouping = grouper.Grouping()
        assert len(grouping.groups) == 0
        g = grouper.Group([course.Student(1, 'Thomas'),
                           course.Student(2, 'Fo'),
                           course.Student(3, 'Dd'),
                           course.Student(4, 'DW')])
        g2 = grouper.Group([course.Student(6, 'R'),
                            course.Student(7, 'D'),
                            course.Student(8, 'F'),
                            course.Student(9, 'G')])
        grouping = grouper.Grouping()
        grouping.add_group(g)
        grouping.add_group(g2)
        length = len(grouping)
        assert length == 2

    def test_str_one_group(self) -> None:
        g1 = grouper.Group([course.Student(1, 'Thomas'),
                            course.Student(2, 'Fo'),
                            course.Student(3, 'Dd'),
                            course.Student(4, 'Dw')])
        grouping = grouper.Grouping()
        grouping.add_group(g1)
        groups = str(grouping)
        assert groups == 'Thomas,Fo,Dd,Dw\n'

    def test_add_group_valid(self) -> None:
        """Group is not in Grouping - all students have different ids"""
        g = grouper.Group([course.Student(1, 'Thomas'),
                           course.Student(2, 'Fo'),
                           course.Student(3, 'Dd'),
                           course.Student(4, 'DW')])
        g2 = grouper.Group([course.Student(6, 'R'),
                            course.Student(7, 'D'),
                            course.Student(8, 'F'),
                            course.Student(9, 'G')])
        grouping = grouper.Grouping()
        grouping.add_group(g)
        Value = grouping.add_group(g2)
        assert Value is True

    def test_get_groups_one_group(self) -> None:
        g = grouper.Group([course.Student(1, 'Thomas'),
                           course.Student(2, 'Fo'),
                           course.Student(3, 'Dd'),
                           course.Student(4, 'DW')])
        grouping = grouper.Grouping()
        grouping.add_group(g)
        lst = grouping.get_groups()
        assert lst == [g]


class TestSurvey:

    def test_len_survey(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        q2 = survey.NumericQuestion(2, 'how', 0, 4)
        q3 = survey.CheckboxQuestion(3, 'why', ['a', 'b', 'c', 'd'])
        questions = [q1, q2, q3]
        s = survey.Survey(questions)
        length = len(s)
        assert length == 3

    def test_contains_true(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        q2 = survey.NumericQuestion(2, 'how', 0, 4)
        q3 = survey.CheckboxQuestion(3, 'why', ['a', 'b', 'c', 'd'])
        questions = [q1, q2, q3]
        s = survey.Survey(questions)
        value = s.__contains__(q1)
        assert value is True

    def test_str_survey(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        questions = [q1]
        s = survey.Survey(questions)
        words = str(s)
        assert words == str(q1) + ','

    def test_get_questions(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        q2 = survey.NumericQuestion(2, 'how', 0, 4)
        q3 = survey.CheckboxQuestion(3, 'why', ['a', 'b', 'c', 'd'])
        questions = [q1, q2, q3]
        s = survey.Survey(questions)
        lst = s.get_questions()
        assert lst == [q1, q2, q3]

    def test_set_criterion(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        s1 = Survey([q1])
        h1 = HeterogeneousCriterion()
        value = s1.set_criterion(h1, q1)
        assert value is True

    def test_set_weight(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        s1 = Survey([q1])
        value = s1.set_weight(2, q1)
        assert value is True

    def test_get_criterion(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        s1 = Survey([q1])
        h1 = HeterogeneousCriterion()
        s1.set_criterion(h1, q1)
        gc = s1._get_criterion(q1)
        assert gc == h1

    def test_get_weight(self) -> None:
        q1 = survey.MultipleChoiceQuestion(1, 'why', ['a', 'b', 'c', 'd'])
        s1 = Survey([q1])
        s1.set_weight(2, q1)
        gw = s1._get_weight(q1)
        assert gw == 2

    def test_score_students(self) -> None:
        s1 = Survey([])
        assert s1.score_students([]) == 0.0

    def test_score_grouping(self) -> None:
        s1 = Survey([])
        g = Group([course.Student(1, 'Thomas'),
                   course.Student(2, 'Fo'),
                   course.Student(3, 'Dd'),
                   course.Student(4, 'DW')])
        g1 = Grouping()
        g1.add_group(g)
        assert s1.score_grouping(g1) == 0.0


if __name__ == '__main__':
    pytest.main(['tests.py'])
