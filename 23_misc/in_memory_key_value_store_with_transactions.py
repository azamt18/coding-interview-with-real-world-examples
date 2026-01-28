
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

    Part 1: basic key-value store
        set | O(1) time | O(1) space
        get | O(1) time | O(1) space
        delete | O(1) time | O(1) space
        overall | O(n), n = keys numbers

    Part 2: single transaction support
        methods: begin(), rollback(), commit()
        isolation level: reads uncommitted changes

        consider:
            1. how to isolate transaction changes
                opt a: copy entire store on begin (expensive)
                opt b: maintain separate "pending changes" map (efficient)
            2. how to handle reads
                opt a: first check pending changes, then fall back to global store
            3. how to handle deletes
                * need a way to distinguish "key deleted in transaction" from "key doesn't exist"
                * use sentinel value or separate deleted keys set
        decisions:
            1. sentinel value for deletes using _DELETED object that's unique marker that cannot collide with other value
            2. lazy copying: don't copy the entire store on begin, track only modified keys in _transaction
            3. read path: check transaction layer first, then global store, ensures read-your-writes consistency within transaction

        begin           | O(1) time | O(1) space
        commit          | O(t) time | O(1) space
        rollback        | O(1) time | O(1) space
        set/get/delete  | O(1) time | O(1) space
        t = transactions count

"""
import unittest

class Database:
    # sentinel value to mark deleted keys
    _DELETED = object()

    def __init__(self):
        self.store: dict[str, str] = {}
        self._transaction: dict[str, str | object] | None = None

    def set(self, key: str, val: str) -> None:
        if self._transaction:
            self._transaction[key] = val
        else:
            self.store[key] = val

    def get(self, key: str) -> str | None:
        if self._transaction:
            if key in self._transaction:
                val = self._transaction[key]
                # check if key was deleted in transaction
                if val is self._DELETED:
                    return None
                return val
            return None
        else:
            if key not in self.store:
                return None
            return self.store[key]

    def delete(self, key: str) -> bool:
        """ Delete key. Returns True if key existed, False otherwise """
        # check if key exists including transaction layer
        exists = self.store.get(key) is not None
        if self._transaction:
            # mark
            self._transaction[key] = self._DELETED
        else:
            del self.store[key]
        return exists

    def begin(self) -> None:
        """ init a new transaction """
        self._transaction = {}

    def commit(self) -> RuntimeError | None:
        """ commit the current transaction """
        if self._transaction is None:
            return RuntimeError("No active transaction")
        # apply all changes to global store
        for key, val in self._transaction.items():
            if val in self._DELETED:
                self.store.pop(key, None)
            else:
                self.store[key] = val
        self._transaction = None
        return None

    def rollback(self) -> RuntimeError | None:
        if self._transaction is None:
            return RuntimeError("No active transaction")
        self._transaction = None
        return None

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