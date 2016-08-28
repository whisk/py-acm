import pytest
import strings.kmp as kmp

# find
def test_find_empty_text():
  assert kmp.find('random-pattern', '') == -1

def test_find_simple():
  assert kmp.find('el', 'On recommend tolerably my belonging or am. Mutual has cannot beauty indeed now sussex merely you') == 27

# find_all
def test_find_all_empty_text():
  assert kmp.find_all('random-pattern', '') == []

def test_find_all_simple():
  assert kmp.find_all('el', 'On recommend tolerably my belonging or am. Mutual has cannot beauty indeed now sussex merely you') == [27, 89]
