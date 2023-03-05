import stack as Stack
import container as Container
import pytest as test


def test_push_pop_height():
    stack1 = Stack.Stack(1, 8)
    stack2 = Stack.Stack(2, 8)

    c1 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c2 = Container.Container(weight=996, description="Costco", on_ship=True)
    c3 = Container.Container(weight=996, description="Costco", on_ship=True)
    c4 = Container.Container(weight=996, description="Costco", on_ship=True)
    c5 = Container.Container(weight=333, description="Walmart", on_ship=True)
    c6 = Container.Container(weight=520, description="Frice", on_ship=True)
    c7 = Container.Container()
    c8 = Container.Container()
    c9 = Container.Container()

    cont_list = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

    stack1.push(c1)
    stack2.push(c4)
    stack1.push(c3)
    stack2.push(c2)
    stack2.push(c6)
    stack2.push(c5)

    assert stack2.get_height() == 4

    assert stack2.pop() == c5
    assert stack2.pop() == c6

    assert stack2.get_height() == 2

    assert stack2.pop() == c2
    assert stack2.pop() == c4

    assert stack2.get_height() == 0

    assert stack1.get_height() == 2

    assert stack1.pop() == c3
    assert stack1.pop() == c1

    for i in range(0, 8):
        stack1.push(cont_list[i])

    with test.raises(IndexError):
        stack1.push(c9)