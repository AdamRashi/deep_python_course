import cProfile
import timeit
import weakref

from memory_profiler import profile


class Teacher:
    """Вспомогательный класс, содержаший циклическую ссылку"""

    def __init__(self, name, course_name):
        self.name = name
        self.course = Course(course_name, self)


class Course:
    """Класс с обычными атрибутами"""

    def __init__(self, title, teacher):
        self.title = title
        self.teacher = teacher


class CourseWithSlots:
    """Класс со слотами"""

    __slots__ = ("title", "teacher")

    def __init__(self, title, teacher):
        self.title = title
        self.teacher = teacher


class CourseWithWeakref:
    """Класс с использованием weakref"""

    def __init__(self, title, teacher):
        self.title = title
        self.teacher = weakref.ref(teacher)


@profile
def instance_creation_comparison(n):
    """
    Функция, которая замеряет время создания пачки экземпляров
    разных классов
    """

    t1 = timeit.timeit(
        "[Course(f'title_{i}', Teacher(f'teacher_{i}', f'title_{i}'))"
        + f"for i in range({n})]",
        setup="from __main__ import Teacher, Course",
        number=1,
    )

    t2 = timeit.timeit(
        "[CourseWithSlots(f'title_{i}', Teacher(f'teacher_{i}', f'title_{i}'))"
        + f"for i in range({n})]",
        setup="from __main__ import Teacher, CourseWithSlots",
        number=1,
    )

    t3 = timeit.timeit(
        "[CourseWithWeakref(f'title_{i}', Teacher(f'teacher_{i}', f'title_{i}'))"
        + f"for i in range({n})]",
        setup="from __main__ import Teacher, CourseWithWeakref",
        number=1,
    )

    print(f"\nВремя создания экземпляров различных классов ({n = })")
    print(f"\tКласс Course: {t1:.6f}")
    print(f"\tКласс CourseWithSlots: {t2:.6f}")
    print(f"\tКласс CourseWithWeakref: {t3:.6f}\n\n")


@profile
def attribute_access_comparison(n):
    """
    Функция, которая замеряет время чтения и изменения атрибутов
    разных классов
    """
    # замер времени доступа и чтения атрибутов для каждого экземпляра
    t1 = timeit.timeit(
        "[course.title for course in courses]",
        setup="from __main__ import courses",
        number=1,
    )
    t2 = timeit.timeit(
        "[setattr(course, 'title', 'Advanced Python') for course in courses]",
        setup="from __main__ import courses",
        number=1,
    )

    t3 = timeit.timeit(
        "[course.title for course in courses_with_slots]",
        setup="from __main__ import courses_with_slots",
        number=1,
    )
    t4 = timeit.timeit(
        "[setattr(course, 'title', 'Advanced Python') for course in courses_with_slots]",
        setup="from __main__ import courses_with_slots",
        number=1,
    )

    t5 = timeit.timeit(
        "[course.title for course in courses_with_weakref]",
        setup="from __main__ import courses_with_weakref",
        number=1,
    )
    t6 = timeit.timeit(
        "[setattr(course, 'title', 'Advanced Python') for course in courses_with_weakref]",
        setup="from __main__ import courses_with_weakref",
        number=1,
    )

    print(f"\nВремя доступа и чтения атрибутов у различных классов ({n = })")
    print(f"\tКласс Course. Чтение: {t1:.6f}, запись: {t2:.6f}")
    print(f"\tКласс CourseWithSlots. Чтение: {t3:.6f}, запись: {t4:.6f}")
    print(f"\tКласс CourseWithWeakref. Чтение: {t5:.6f}, запись: {t6:.6f}")


if __name__ == "__main__":
    N = 100000

    instance_creation_comparison(N)

    courses = [Course("Python", Teacher("John Doe", "Python")) for _ in range(N)]
    courses_with_slots = [
        CourseWithSlots("Python", Teacher("John Doe", "Python")) for _ in range(N)
    ]
    courses_with_weakref = [
        CourseWithWeakref("Python", Teacher("John Doe", "Python")) for _ in range(N)
    ]

    attribute_access_comparison(N)

    cProfile.run("instance_creation_comparison(N)")
    cProfile.run("attribute_access_comparison(N)")
