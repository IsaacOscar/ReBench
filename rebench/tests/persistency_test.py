# Copyright (c) 2009-2014 Stefan Marr <http://www.stefan-marr.de/>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
from datetime import datetime

from .rebench_test_case import ReBenchTestCase

from ..persistence  import DataStore

from ..model.benchmark import Benchmark
from ..model.benchmark_suite import BenchmarkSuite
from ..model.exp_run_details import ExpRunDetails
from ..model.measurement      import Measurement
from ..model.run_id           import RunId
from ..model.virtual_machine  import VirtualMachine


class PersistencyTest(ReBenchTestCase):

    def test_de_serialization(self):
        data_store = DataStore(self._ui)
        vm = VirtualMachine("MyVM", '', '',
                            None, None, None, None, None)
        suite = BenchmarkSuite("MySuite", vm, '', '', None, None,
                               None, None, None, None)
        benchmark = Benchmark("Test Bench [>", "Test Bench [>", None,
                              suite, None, None, ExpRunDetails.default(), None, data_store)

        run_id = RunId(benchmark, 1000, 44, 'sdf sdf sdf sdfsf')
        timestamp = datetime.now().replace(microsecond=0)
        measurement = Measurement(2222.2222, 'ms', run_id, 'foobar crit',
                                  timestamp)

        serialized = measurement.as_str_list()
        deserialized = Measurement.from_str_list(data_store, serialized)

        self.assertEqual(deserialized.criterion, measurement.criterion)
        self.assertEqual(deserialized.value, measurement.value)
        self.assertEqual(deserialized.unit, measurement.unit)
        self.assertAlmostEqual(deserialized.timestamp, measurement.timestamp)

        self.assertEqual(deserialized.run_id, measurement.run_id)
