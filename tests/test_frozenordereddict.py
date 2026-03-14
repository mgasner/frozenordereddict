from collections import OrderedDict
from unittest import TestCase

from frozenordereddict import FrozenOrderedDict


class TestFrozenOrderedDict(TestCase):
    ITEMS_1 = (
        ("b", 2),
        ("a", 1),
    )
    ITEMS_2 = (
        ("d", 4),
        ("c", 3),
    )

    ODICT_1 = OrderedDict(ITEMS_1)
    ODICT_2 = OrderedDict(ITEMS_2)

    def test_init_from_items(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(list(self.ITEMS_1), list(fod.items()))

    def test_init_from_ordereddict(self):
        fod = FrozenOrderedDict(self.ODICT_1)
        self.assertEqual(list(self.ITEMS_1), list(fod.items()))

    def test_init_empty(self):
        fod = FrozenOrderedDict()
        self.assertEqual(len(fod), 0)
        self.assertEqual(list(fod.items()), [])

    def test_init_from_kwargs(self):
        fod = FrozenOrderedDict(x=1, y=2)
        self.assertIn("x", fod)
        self.assertIn("y", fod)
        self.assertEqual(fod["x"], 1)
        self.assertEqual(fod["y"], 2)

    def test_setitem(self):
        def doit():
            fod = FrozenOrderedDict()
            fod[1] = "b"

        self.assertRaises(TypeError, doit)

    def test_delitem(self):
        def doit():
            fod = FrozenOrderedDict(self.ITEMS_1)
            del fod[1]

        self.assertRaises(TypeError, doit)

    def test_getitem(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(fod["b"], 2)
        self.assertEqual(fod["a"], 1)

    def test_getitem_missing_key(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        with self.assertRaises(KeyError):
            fod["missing"]

    def test_iter_preserves_order(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(list(fod), ["b", "a"])

    def test_len(self):
        self.assertEqual(len(FrozenOrderedDict()), 0)
        self.assertEqual(len(FrozenOrderedDict(self.ITEMS_1)), 2)
        self.assertEqual(len(FrozenOrderedDict(self.ITEMS_1 + self.ITEMS_2)), 4)

    def test_contains(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertIn("b", fod)
        self.assertIn("a", fod)
        self.assertNotIn("z", fod)

    def test_keys(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(list(fod.keys()), ["b", "a"])

    def test_values(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(list(fod.values()), [2, 1])

    def test_items(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(list(fod.items()), [("b", 2), ("a", 1)])

    def test_get_existing_key(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(fod.get("b"), 2)

    def test_get_missing_key_default(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertIsNone(fod.get("missing"))
        self.assertEqual(fod.get("missing", 42), 42)

    def test_hash_equal_dicts_same_hash(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(hash(fod1), hash(fod2))

    def test_hash_is_cached(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        h1 = hash(fod)
        h2 = hash(fod)
        self.assertEqual(h1, h2)

    def test_hash_different_values_different_hash(self):
        fod1 = FrozenOrderedDict([("a", 1), ("b", 2)])
        fod2 = FrozenOrderedDict([("a", 3), ("b", 4)])
        self.assertNotEqual(hash(fod1), hash(fod2))

    def test_hash_empty(self):
        fod = FrozenOrderedDict()
        self.assertEqual(hash(fod), 0)

    def test_usable_as_dict_key(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        d = {fod: "value"}
        self.assertEqual(d[fod], "value")

    def test_usable_in_set(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = FrozenOrderedDict(self.ITEMS_1)
        s = {fod1, fod2}
        self.assertEqual(len(s), 1)

    def test_equality(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = FrozenOrderedDict(self.ITEMS_1)
        self.assertEqual(fod1, fod2)

    def test_inequality_different_values(self):
        fod1 = FrozenOrderedDict([("a", 1)])
        fod2 = FrozenOrderedDict([("a", 2)])
        self.assertNotEqual(fod1, fod2)

    def test_inequality_different_keys(self):
        fod1 = FrozenOrderedDict([("a", 1), ("b", 2)])
        fod2 = FrozenOrderedDict([("x", 1), ("y", 2)])
        self.assertNotEqual(fod1, fod2)

    def test_repr(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        r = repr(fod)
        self.assertTrue(r.startswith("FrozenOrderedDict("))
        self.assertIn("'b'", r)
        self.assertIn("'a'", r)

    def test_repr_empty(self):
        fod = FrozenOrderedDict()
        self.assertEqual(repr(fod), "FrozenOrderedDict([])")

    def test_copy_no_items(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = fod1.copy()

        self.assertNotEqual(id(fod1), id(fod2))
        self.assertEqual(list(fod1.items()), list(fod2.items()))
        self.assertEqual(repr(fod1), repr(fod2))
        self.assertEqual(len(fod1), len(fod2))
        self.assertEqual(hash(fod1), hash(fod2))

    def test_copy_tuple_items(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = fod1.copy(self.ITEMS_2)

        self.assertNotEqual(id(fod1), id(fod2))
        self.assertEqual(
            list(fod1.items()) + list(self.ITEMS_2), list(fod2.items())
        )

    def test_copy_ordereddict_items(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = fod1.copy(self.ODICT_2)

        self.assertNotEqual(id(fod1), id(fod2))
        self.assertEqual(
            list(fod1.items()) + list(self.ITEMS_2), list(fod2.items())
        )

    def test_copy_kwargs(self):
        fod1 = FrozenOrderedDict(self.ITEMS_1)
        fod2 = fod1.copy(**self.ODICT_2)

        self.assertNotEqual(id(fod1), id(fod2))
        expected = dict(list(fod1.items()) + list(self.ODICT_2.items()))
        self.assertEqual(expected, dict(fod2))

    def test_copy_returns_frozenordereddict(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        copy = fod.copy()
        self.assertIsInstance(copy, FrozenOrderedDict)

    def test_no_mutating_methods(self):
        fod = FrozenOrderedDict(self.ITEMS_1)
        for method in ("pop", "popitem", "clear", "update", "setdefault"):
            self.assertFalse(
                hasattr(fod, method),
                f"FrozenOrderedDict should not have {method}()",
            )

    def test_isinstance_mapping(self):
        from collections.abc import Mapping

        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertIsInstance(fod, Mapping)

    def test_not_isinstance_mutable_mapping(self):
        from collections.abc import MutableMapping

        fod = FrozenOrderedDict(self.ITEMS_1)
        self.assertNotIsInstance(fod, MutableMapping)
