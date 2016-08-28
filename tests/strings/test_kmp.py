import pytest
import strings.kmp as kmp

def test_find_empty_text():
  assert kmp.find('random-pattern', '') == -1

def test_find_all_empty_text():
  assert kmp.find_all('random-pattern', '') == []
