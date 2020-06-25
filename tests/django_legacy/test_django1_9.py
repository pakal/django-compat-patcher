import copy
import datetime
import os
import pickle
import time
import unittest
import six

from django.test import SimpleTestCase


class SortedDictTests(SimpleTestCase):
    def setUp(self):
        from django.utils.datastructures import SortedDict

        super(SortedDictTests, self).setUp()
        self.d1 = SortedDict()
        self.d1[7] = "seven"
        self.d1[1] = "one"
        self.d1[9] = "nine"

        self.d2 = SortedDict()
        self.d2[1] = "one"
        self.d2[9] = "nine"
        self.d2[0] = "nil"
        self.d2[7] = "seven"

    def test_basic_methods(self):
        self.assertEqual(list(six.iterkeys(self.d1)), [7, 1, 9])
        self.assertEqual(list(six.itervalues(self.d1)), ["seven", "one", "nine"])
        self.assertEqual(
            list(six.iteritems(self.d1)), [(7, "seven"), (1, "one"), (9, "nine")]
        )

    def test_overwrite_ordering(self):
        """ Overwriting an item keeps its place. """
        self.d1[1] = "ONE"
        self.assertEqual(list(six.itervalues(self.d1)), ["seven", "ONE", "nine"])

    def test_append_items(self):
        """ New items go to the end. """
        self.d1[0] = "nil"
        self.assertEqual(list(six.iterkeys(self.d1)), [7, 1, 9, 0])

    def test_delete_and_insert(self):
        """
        Deleting an item, then inserting the same key again will place it
        at the end.
        """
        del self.d2[7]
        self.assertEqual(list(six.iterkeys(self.d2)), [1, 9, 0])
        self.d2[7] = "lucky number 7"
        self.assertEqual(list(six.iterkeys(self.d2)), [1, 9, 0, 7])

    if six.PY2:

        def test_change_keys(self):
            """
            Changing the keys won't do anything, it's only a copy of the
            keys dict.
            This test doesn't make sense under Python 3 because keys is
            an iterator.
            """
            k = self.d2.keys()
            k.remove(9)
            self.assertEqual(self.d2.keys(), [1, 9, 0, 7])

    def test_init_keys(self):
        """
        Initialising a SortedDict with two keys will just take the first one.
        A real dict will actually take the second value so we will too, but
        we'll keep the ordering from the first key found.
        """
        from django.utils.datastructures import SortedDict

        tuples = ((2, "two"), (1, "one"), (2, "second-two"))
        d = SortedDict(tuples)

        self.assertEqual(list(six.iterkeys(d)), [2, 1])

        real_dict = dict(tuples)
        self.assertEqual(sorted(six.itervalues(real_dict)), ["one", "second-two"])

        # Here the order of SortedDict values *is* what we are testing
        self.assertEqual(list(six.itervalues(d)), ["second-two", "one"])

    def test_overwrite(self):
        self.d1[1] = "not one"
        self.assertEqual(self.d1[1], "not one")
        self.assertEqual(
            list(six.iterkeys(self.d1)), list(six.iterkeys(self.d1.copy()))
        )

    def test_append(self):
        self.d1[13] = "thirteen"
        self.assertEqual(
            repr(self.d1), "{7: 'seven', 1: 'one', 9: 'nine', 13: 'thirteen'}"
        )

    def test_pop(self):
        self.assertEqual(self.d1.pop(1, "missing"), "one")
        self.assertEqual(self.d1.pop(1, "missing"), "missing")

        # We don't know which item will be popped in popitem(), so we'll
        # just check that the number of keys has decreased.
        l = len(self.d1)
        self.d1.popitem()
        self.assertEqual(l - len(self.d1), 1)

    def test_dict_equality(self):
        from django.utils.datastructures import SortedDict

        d = SortedDict((i, i) for i in range(3))
        self.assertEqual(d, {0: 0, 1: 1, 2: 2})

    def test_tuple_init(self):
        from django.utils.datastructures import SortedDict

        d = SortedDict(((1, "one"), (0, "zero"), (2, "two")))
        self.assertEqual(repr(d), "{1: 'one', 0: 'zero', 2: 'two'}")

    def test_pickle(self):
        self.assertEqual(
            pickle.loads(pickle.dumps(self.d1, 2)), {7: "seven", 1: "one", 9: "nine"}
        )

    def test_copy(self):
        from django.utils.datastructures import SortedDict

        orig = SortedDict(((1, "one"), (0, "zero"), (2, "two")))
        copied = copy.copy(orig)
        self.assertEqual(list(six.iterkeys(orig)), [1, 0, 2])
        self.assertEqual(list(six.iterkeys(copied)), [1, 0, 2])

    def test_clear(self):
        self.d1.clear()
        self.assertEqual(self.d1, {})
        self.assertEqual(self.d1.keyOrder, [])

    def test_reversed(self):
        self.assertEqual(list(self.d1), [7, 1, 9])
        self.assertEqual(list(self.d2), [1, 9, 0, 7])
        self.assertEqual(list(reversed(self.d1)), [9, 1, 7])
        self.assertEqual(list(reversed(self.d2)), [7, 0, 9, 1])


class MergeDictTests(SimpleTestCase):
    def test_simple_mergedict(self):
        from django.utils.datastructures import MergeDict

        d1 = {
            "chris": "cool",
            "camri": "cute",
            "cotton": "adorable",
            "tulip": "snuggable",
            "twoofme": "firstone",
        }

        d2 = {
            "chris2": "cool2",
            "camri2": "cute2",
            "cotton2": "adorable2",
            "tulip2": "snuggable2",
        }

        d3 = {
            "chris3": "cool3",
            "camri3": "cute3",
            "cotton3": "adorable3",
            "tulip3": "snuggable3",
        }

        md = MergeDict(d1, d2, d3)

        self.assertEqual(md["chris"], "cool")
        self.assertEqual(md["camri"], "cute")
        self.assertEqual(md["twoofme"], "firstone")

        md2 = md.copy()
        self.assertEqual(md2["chris"], "cool")

    def test_mergedict_merges_multivaluedict(self):
        """ MergeDict can merge MultiValueDicts """
        from django.utils.datastructures import MergeDict, MultiValueDict

        multi1 = MultiValueDict({"key1": ["value1"], "key2": ["value2", "value3"]})

        multi2 = MultiValueDict({"key2": ["value4"], "key4": ["value5", "value6"]})

        mm = MergeDict(multi1, multi2)

        # Although 'key2' appears in both dictionaries,
        # only the first value is used.
        self.assertEqual(mm.getlist("key2"), ["value2", "value3"])
        self.assertEqual(mm.getlist("key4"), ["value5", "value6"])
        self.assertEqual(mm.getlist("undefined"), [])

        self.assertEqual(sorted(six.iterkeys(mm)), ["key1", "key2", "key4"])
        self.assertEqual(len(list(six.itervalues(mm))), 3)

        self.assertIn("value1", six.itervalues(mm))

        self.assertEqual(
            sorted(six.iteritems(mm), key=lambda k: k[0]),
            [("key1", "value1"), ("key2", "value3"), ("key4", "value6")],
        )

        self.assertEqual(
            [(k, mm.getlist(k)) for k in sorted(mm)],
            [
                ("key1", ["value1"]),
                ("key2", ["value2", "value3"]),
                ("key4", ["value5", "value6"]),
            ],
        )

    def test_bool_casting(self):
        from django.utils.datastructures import MergeDict

        empty = MergeDict({}, {}, {})
        not_empty = MergeDict({}, {}, {"key": "value"})
        self.assertFalse(empty)
        self.assertTrue(not_empty)

    def test_key_error(self):
        """
        Test that the message of KeyError contains the missing key name.
        """
        from django.utils.datastructures import MergeDict

        d1 = MergeDict({"key1": 42})
        with six.assertRaisesRegex(self, KeyError, "key2"):
            d1["key2"]


class TzinfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TzinfoTests, cls).setUpClass()
        cls.old_TZ = os.environ.get("TZ")
        os.environ["TZ"] = "US/Eastern"

        try:
            # Check if a timezone has been set
            time.tzset()
            cls.tz_tests = True
        except AttributeError:
            # No timezone available. Don't run the tests that require a TZ
            cls.tz_tests = False

    @classmethod
    def tearDownClass(cls):
        if cls.old_TZ is None:
            del os.environ["TZ"]
        else:
            os.environ["TZ"] = cls.old_TZ

        # Cleanup - force re-evaluation of TZ environment variable.
        if cls.tz_tests:
            time.tzset()
        super(TzinfoTests, cls).tearDownClass()

    def test_fixedoffset(self):
        from django.utils.tzinfo import FixedOffset

        self.assertEqual(repr(FixedOffset(0)), "+0000")
        self.assertEqual(repr(FixedOffset(60)), "+0100")
        self.assertEqual(repr(FixedOffset(-60)), "-0100")
        self.assertEqual(repr(FixedOffset(280)), "+0440")
        self.assertEqual(repr(FixedOffset(-280)), "-0440")
        self.assertEqual(repr(FixedOffset(-78.4)), "-0118")
        self.assertEqual(repr(FixedOffset(78.4)), "+0118")
        self.assertEqual(repr(FixedOffset(-5.5 * 60)), "-0530")
        self.assertEqual(repr(FixedOffset(5.5 * 60)), "+0530")
        self.assertEqual(repr(FixedOffset(-0.5 * 60)), "-0030")
        self.assertEqual(repr(FixedOffset(0.5 * 60)), "+0030")

    def test_16899(self):
        if not self.tz_tests:
            return
        from django.utils.tzinfo import LocalTimezone

        ts = 1289106000
        # Midnight at the end of DST in US/Eastern: 2010-11-07T05:00:00Z
        dt = datetime.datetime.utcfromtimestamp(ts)
        # US/Eastern -- we force its representation to "EST"
        tz = LocalTimezone(dt + datetime.timedelta(days=1))
        self.assertEqual(
            repr(datetime.datetime.fromtimestamp(ts - 3600, tz)),
            "datetime.datetime(2010, 11, 7, 0, 0, tzinfo=EST)",
        )
        self.assertEqual(
            repr(datetime.datetime.fromtimestamp(ts, tz)),
            "datetime.datetime(2010, 11, 7, 1, 0, tzinfo=EST)",
        )
        self.assertEqual(
            repr(datetime.datetime.fromtimestamp(ts + 3600, tz)),
            "datetime.datetime(2010, 11, 7, 1, 0, tzinfo=EST)",
        )

    def test_copy(self):
        from django.utils.tzinfo import FixedOffset, LocalTimezone

        now = datetime.datetime.now()
        self.assertIsInstance(copy.copy(FixedOffset(90)), FixedOffset)
        self.assertIsInstance(copy.copy(LocalTimezone(now)), LocalTimezone)

    def test_deepcopy(self):
        from django.utils.tzinfo import FixedOffset, LocalTimezone

        now = datetime.datetime.now()
        self.assertIsInstance(copy.deepcopy(FixedOffset(90)), FixedOffset)
        self.assertIsInstance(copy.deepcopy(LocalTimezone(now)), LocalTimezone)

    def test_pickling_unpickling(self):
        from django.utils.tzinfo import FixedOffset, LocalTimezone

        now = datetime.datetime.now()
        self.assertIsInstance(pickle.loads(pickle.dumps(FixedOffset(90))), FixedOffset)
        self.assertIsInstance(
            pickle.loads(pickle.dumps(LocalTimezone(now))), LocalTimezone
        )
