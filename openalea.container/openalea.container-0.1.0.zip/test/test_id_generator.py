from nose.tools import assert_raises

from openalea.container.id_generator import (IdMaxGenerator,
                                             IdSetGenerator,
                                             IdGenerator,
                                             IdListGenerator)


def test_max_gen_start_at_zero():
    gen = IdMaxGenerator()
    assert gen.get_id() == 0


def test_max_gen_does_not_return_twice_the_same_value():
    gen = IdMaxGenerator()
    pid0 = gen.get_id()
    assert gen.get_id() > pid0


def test_max_gen_raise_error_if_asked_twice_for_the_same_id():
    gen = IdMaxGenerator()
    gen.get_id(10)
    assert_raises(IndexError, lambda: gen.get_id(10))


def test_max_gen_always_return_increasing_ids():
    gen = IdMaxGenerator()
    pid0 = gen.get_id(11)
    pid1 = gen.get_id()
    assert pid1 > pid0
    gen.release_id(pid1)
    assert gen.get_id() > pid1


def test_max_gen_clear_restart_from_zero():
    gen = IdMaxGenerator()
    pid0 = gen.get_id(12)
    gen.clear()
    assert gen.get_id() == 0
    assert gen.get_id(pid0) == pid0


def test_set_gen_start_at_zero():
    gen = IdSetGenerator()
    assert gen.get_id() == 0


def test_set_gen_does_not_return_twice_the_same_value():
    gen = IdSetGenerator()
    pid0 = gen.get_id()
    assert gen.get_id() != pid0


def test_set_gen_raise_error_if_asked_twice_for_the_same_id():
    gen = IdSetGenerator()
    gen.get_id(10)
    assert_raises(IndexError, lambda: gen.get_id(10))


def test_set_gen_returns_available_ids():
    gen = IdSetGenerator()
    pid = gen.get_id(10)
    assert gen.get_id() < pid


def test_set_gen_release_id_render_it_available():
    gen = IdSetGenerator()
    pid = gen.get_id(16)
    gen.release_id(pid)
    assert gen.get_id(pid) == pid


def test_set_gen_release_id_raise_error_if_id_not_used_already():
    gen = IdSetGenerator()
    gen.get_id(16)
    assert_raises(IndexError, lambda: gen.release_id(20))
    assert_raises(IndexError, lambda: gen.release_id(0))


def test_set_gen_clear_restart_from_zero():
    gen = IdSetGenerator()
    pid0 = gen.get_id(12)
    gen.clear()
    assert gen.get_id() == 0
    assert gen.get_id(pid0) == pid0


def test_id_gen_exists():
    gen = IdGenerator()
    assert gen.get_id(10) == 10


def test_list_gen_start_at_zero():
    gen = IdListGenerator()
    assert gen.get_id() == 0


def test_list_gen_does_not_return_twice_the_same_value():
    gen = IdListGenerator()
    pid0 = gen.get_id()
    assert gen.get_id() != pid0


def test_list_gen_raise_error_if_asked_twice_for_the_same_id():
    gen = IdListGenerator()
    gen.get_id(10)
    assert_raises(IndexError, lambda: gen.get_id(10))


def test_list_gen_returns_available_ids():
    gen = IdListGenerator()
    pid = gen.get_id(10)
    assert gen.get_id() < pid


def test_list_gen_release_id_render_it_available():
    gen = IdListGenerator()
    pid = gen.get_id(16)
    gen.release_id(pid)
    assert gen.get_id(pid) == pid


def test_list_gen_release_id_raise_error_if_id_not_used_already():
    gen = IdListGenerator()
    gen.get_id(16)
    assert_raises(IndexError, lambda: gen.release_id(20))
    assert_raises(IndexError, lambda: gen.release_id(0))


def test_list_gen_clear_restart_from_zero():
    gen = IdListGenerator()
    pid0 = gen.get_id(12)
    gen.clear()
    assert gen.get_id() == 0
    assert gen.get_id(pid0) == pid0
