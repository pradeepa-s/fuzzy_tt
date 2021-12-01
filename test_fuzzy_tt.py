import pytest
import fuzzy_tt


class TestFuzzyTt:
    def setup_method(self, method):
        self._store = fuzzy_tt.InterestsStore()

    def teardown_method(self, method):
        pass


class TestAddInterest(TestFuzzyTt):
    def test_add_interest_adds_one_interest(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        assert self._store.find("Interest1")

    def test_add_interest_adds_two_interests(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.add_interest("Interest2", self._store)
        assert self._store.find("Interest1")
        assert self._store.find("Interest2")

    def test_add_interest_shall_not_add_same_interest_twice(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.add_interest("Interest1", self._store)
        assert self._store.count() == 1


class TestLogTime(TestFuzzyTt):
    def test_log_time_shall_update_time(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.log_time(self._store, "Interest1", 10)
        assert "Interest1 (Logged 10 minutes)" in str(self._store)

    def test_log_time_shall_accumulate_time(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.log_time(self._store, "Interest1", 10)
        fuzzy_tt.log_time(self._store, "Interest1", 100)
        assert "Interest1 (Logged 110 minutes)" in str(self._store)

    def test_log_time_shall_add_time_to_correct_interest(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.add_interest("Interest2", self._store)
        fuzzy_tt.log_time(self._store, "Interest1", 10)
        fuzzy_tt.log_time(self._store, "Interest2", 100)
        assert "Interest1 (Logged 10 minutes)" in str(self._store)
        assert "Interest2 (Logged 100 minutes)" in str(self._store)


class TestPrettyPrint(TestFuzzyTt):
    def test_print_single_interest(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.log_time(self._store, "Interest1", 10)
        assert str(self._store) == '''[1]: Interest1 (Logged 10 minutes)\n'''

    def test_print_multiple_interests(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.add_interest("Interest2", self._store)
        assert str(self._store) == '''[1]: Interest1 (Logged 0 minutes)
[2]: Interest2 (Logged 0 minutes)\n'''

    def test_sort_before_print(self):
        fuzzy_tt.add_interest("Interest1", self._store)
        fuzzy_tt.add_interest("Interest2", self._store)
        fuzzy_tt.log_time(self._store, "Interest1", 100)
        fuzzy_tt.log_time(self._store, "Interest2", 10)
        assert str(self._store) == '''[1]: Interest2 (Logged 10 minutes)
[2]: Interest1 (Logged 100 minutes)\n'''
