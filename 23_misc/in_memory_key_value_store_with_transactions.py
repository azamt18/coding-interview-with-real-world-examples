
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

    Part 3: nested transaction support
        consider:
            1. child transaction inherits parent state
            2. changes in child transactions are visible to that child
            3. when child commits, its changes merged into parent
            4. when child rollbacks, its changes are discarded, parent is unaffected
            5. when parent rollbacks, all child changes are discarded
            6. only outermost transaction commits do changes to global store

        key design: stack of transaction layers

            transaction 3 <-- current/innermost
            -------------
            transaction 2
            -------------
            transaction 1
            -------------
            global store

            writes: always to top of stack
            reads: search from bottom, return first match
            commits: pop top and merge into layer below
            rollbacks: pop top and discard

    Follow-ups:
        1. thread-safe
            a. global lock: simple, but limits concurrency
            b. read-write lock: allow concurrent reads, exclusive writes
            c. per-transaction isolation: each thread gets its own transaction
        2. persistence
            a. wal (write-ahead log) for durability
            b. snapshot + wal for recovery
            c. background flushing for performance
        3. memory limits
            a. LRU eviction policy
            b. disk-backed storage with memory cache
            c. compression for cold data
        4. transaction timeout
            a. add timeout param to begin()
            b. background thread to abort long-running transactions
            c. resource cleanup on timeout

"""
import unittest

class Database:
    # sentinel value to mark deleted keys
    _DELETED = object()

    def __init__(self):
        self._store: dict[str, str] = {}
        self._transaction_stack: list[dict[str, str | object]] = []

    def get_current_transaction(self) -> dict[str, str | object] | None:
        return self._transaction_stack[-1] if self._transaction_stack else None

    def set(self, key: str, val: str) -> None:
        current_transaction = self.get_current_transaction()
        if current_transaction:
            current_transaction[key] = val
        else:
            self._store[key] = val

    def get(self, key: str) -> str | None:
        """ search key from newest (top) to oldest (bottom) """
        for transaction in reversed(self._transaction_stack):
            if key in transaction:
                val = transaction[key]
                # check if key was deleted in transaction
                if val is self._DELETED:
                    return None
                return val
            return None
        # full search from global store
        return self._store[key]

    def delete(self, key: str) -> bool:
        """ delete key in current transaction """
        # check if key exists including transaction layer
        exists = self.get(key) is not None
        current_transaction = self.get_current_transaction()

        if current_transaction:
            # mark for soft delete
            current_transaction[key] = self._DELETED
        else:
            if key in self._store:
                del self._store[key]

        return exists

    def begin(self) -> None:
        """ start a new nested transaction """
        self._transaction_stack.append({})

    def commit(self) -> RuntimeError | None:
        """ commit the current transaction
            - if inner: merge into parent transaction
            - if outermost: merge into global store
        """

        if self._transaction_stack is None:
            return RuntimeError("No active transaction")

        current_transaction = self._transaction_stack.pop()
        if self._transaction_stack:
            # inner -> merge into parent
            parent = self._transaction_stack[-1]
            for key, val in current_transaction.items():
                parent[key] = val
        else:
            # outermost -> merge into global store
            for key, val in current_transaction.items():
                if val in self._DELETED:
                    self._store.pop(key, None)
                else:
                    self._store[key] = val
        return None

    def rollback(self) -> RuntimeError | None:
        """ rollback current transaction, discard its changes """
        if self._transaction_stack is None:
            return RuntimeError("No active transaction")
        self._transaction_stack.pop()
        return None

    def test_set_and_get(self):
        """ test function """
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