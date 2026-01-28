
"""
    Consider:
    1. transaction isolations - uncommitted changes shouldn't affect global store
    2. state management - track changes within a transaction maintaining a rollbock
    3. extensibility

    Part 1: basic key-value store
    Part 2: single transaction support
    Part 3: nested transaction

    Alternatives:
    1. full copy to begin
    2. undo log
"""
import unittest

class Database:
    def __init__(self):
        self.store: dict[str, str] = {}

    def set(self, key: str, val: str) -> None:
        self.store[key] = val

    def get(self, key: str) -> str | None:
        if key not in self.store:
            return None
        return self.store[key]

    def delete(self, key: str) -> bool:
        if key not in self.store:
            return False
        del self.store[key]
        return True

    def test_set_and_get(self):
        db = Database()
        db.set("foo", "bar")
        assert db.get("foo") == "bar"


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_set_and_get(self):
        self.db.set("foo", "bar")
        self.assertEqual(self.db.get("foo"), "bar")

if __name__ == "__main__":
    unittest.main()