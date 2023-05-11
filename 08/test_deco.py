from profiler_deco import profile_deco


@profile_deco
def add(x, y):
    print(f"{x} + {y} = {x + y}")


@profile_deco
def sub(x, y):
    print(f"{x} + {y} = {x +- y}")


if __name__ == "__main__":
    add(2, 1)
    add(4, 6)

    add.print_stat()
    sub.print_stat()
