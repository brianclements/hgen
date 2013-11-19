import unittest
import csv
import StringIO
from hgen.hgen import num_to_new_base
from hgen.hgen import base_num_to_num
from hgen.hgen import int2alpha
from hgen.hgen import alpha2int
from hgen.hgen import SpreadSheet


class TestNumToNewBase(unittest.TestCase):
    def test_num_to_new_base(self):
        self.assertEqual([0], num_to_new_base(0, 26))
        self.assertEqual([1], num_to_new_base(1, 26))
        self.assertEqual([26], num_to_new_base(26, 26))
        self.assertEqual([1, 1], num_to_new_base(26 + 1, 26))
        self.assertEqual([1, 26], num_to_new_base(26 * 2, 26))
        self.assertEqual([2, 1], num_to_new_base(26 * 2 + 1, 26))
        self.assertEqual([2, 26], num_to_new_base(26 * 3, 26))
        self.assertEqual([3, 1], num_to_new_base(26 * 3 + 1, 26))
        self.assertEqual([3, 26], num_to_new_base(26 * 4, 26))


class TestBaseNumToNum(unittest.TestCase):
    def test_base_num_to_num(self):
        self.assertEqual(0, base_num_to_num([0], 26))
        self.assertEqual(1, base_num_to_num([1], 26))
        self.assertEqual(26, base_num_to_num([26], 26))
        self.assertEqual(26 + 1, base_num_to_num([1, 1], 26))
        self.assertEqual(26 * 2, base_num_to_num([1, 26], 26))
        self.assertEqual(26 * 2 + 1, base_num_to_num([2, 1], 26))
        self.assertEqual(26 * 3, base_num_to_num([2, 26], 26))
        self.assertEqual(26 * 3 + 1, base_num_to_num([3, 1], 26))
        self.assertEqual(26 * 4, base_num_to_num([3, 26], 26))
        self.assertRaises(TypeError, lambda: base_num_to_num(1, 26))


class TestInt2alpha(unittest.TestCase):
    def test_int2alpha(self):
        self.assertEqual('', int2alpha(0))
        self.assertEqual('A', int2alpha(1))
        self.assertEqual('Z', int2alpha(26))
        self.assertEqual('AA', int2alpha(27))
        self.assertEqual('AZ', int2alpha(26 * 2))
        self.assertEqual('BA', int2alpha(26 * 2 + 1))
        self.assertEqual('BZ', int2alpha(26 * 3))
        self.assertEqual('CA', int2alpha(26 * 3 + 1))
        self.assertEqual('CZ', int2alpha(26 * 4))


class TestAlpha2int(unittest.TestCase):
    def test_alpha2int(self):
        self.assertEqual(0, alpha2int(''))
        self.assertEqual(1, alpha2int('A'))
        self.assertEqual(26, alpha2int('Z'))
        self.assertEqual(27, alpha2int('AA'))
        self.assertEqual(26 * 2, alpha2int('AZ'))
        self.assertEqual(26 * 2 + 1, alpha2int('BA'))
        self.assertEqual(26 * 3, alpha2int('BZ'))
        self.assertEqual(26 * 3 + 1, alpha2int('CA'))
        self.assertEqual(26 * 4, alpha2int('CZ'))


class TestSpreadSheet(unittest.TestCase):
    def make_fake_csv(self, data):
        '''
        Return a populated fake csv file-object for testing
        '''
        fake_csv = StringIO.StringIO()
        fake_writer = csv.writer(fake_csv, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_ALL, lineterminator='\n')
        fake_writer.writerows(data)
        fake_csv.seek(0)
        return fake_csv

    def setUp(self):
        self.headers = []
        self.table = [
            ['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6', 'Col7', 'Col8'],
            ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7', 'val8'],
            ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7', 'val8'],
            ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7', 'val8']]
        self.populations = [
            ['sec', 'a', 'a'],
            ['sec1', 'b', 'd'],
            ['sec2', 'e', 'f'],
            ['sec3', 'g', 'h']]
        self.headers = [
            'SEC_A', 'SEC1_B', 'SEC1_C', 'SEC1_D',
            'SEC2_E', 'SEC2_F', 'SEC3_G', 'SEC3_H']

    def test___init__(self):
        temp_csv = self.make_fake_csv(self.table)
        spread_sheet = SpreadSheet(temp_csv)

        self.assertEqual(
            self.table,
            spread_sheet.table)

    def test_create_headers(self):
        target_headers = [
            'SEC_A', 'SEC1_B', 'SEC1_C', 'SEC1_D',
            'SEC2_E', 'SEC2_F', 'SEC3_G', 'SEC3_H']

        temp_csv = self.make_fake_csv(self.table)
        spread_sheet = SpreadSheet(temp_csv)

        spread_sheet.create_headers(self.populations)
        self.assertEqual(target_headers, spread_sheet.headers)

    def test_lookup_header(self):
        lookup_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        temp_csv = self.make_fake_csv(self.table)
        spread_sheet = SpreadSheet(temp_csv)
        spread_sheet.headers = self.headers
        for ltr in lookup_list:
            self.assertEqual(
                self.headers[lookup_list.index(ltr)],
                spread_sheet.lookup_header(ltr))

    def test_lookup_data_point(self):
        temp_csv = self.make_fake_csv(self.table)
        spread_sheet = SpreadSheet(temp_csv)

        test_columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for column in test_columns:
            for row in range(1, 5):
                self.assertEqual(
                    self.table[row - 1][test_columns.index(column)],
                    spread_sheet.lookup_data_point(column, row))

    def test_select_population_data(self):
        read_csv = self.make_fake_csv(self.table)
        spread_sheet = SpreadSheet(read_csv)
        spread_sheet.headers = self.headers

        empty_list = []

        # Test 1 attempt
        write_csv_file = self.make_fake_csv(empty_list)
        spread_sheet.select_population_data(write_csv_file, 'sec', 'sec3')

        # Test 1 target
        test1_target = [
            ['SEC_A', 'SEC3_G', 'SEC3_H'],
            ['Col1', 'Col7', 'Col8'],
            ['val1', 'val7', 'val8'],
            ['val1', 'val7', 'val8'],
            ['val1', 'val7', 'val8']]
        target_file = self.make_fake_csv(empty_list)
        filewriter = csv.writer(target_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL, lineterminator='\n')
        for row in test1_target:
                filewriter.writerow(row)
        self.assertEqual(
            write_csv_file.getvalue(),
            target_file.getvalue())

        # Test 2 attempt
        write_csv_file = self.make_fake_csv(empty_list)
        spread_sheet.select_population_data(write_csv_file, 'sec', 'sec2')

        # Test 2 target
        test1_target = [
            ['SEC_A', 'SEC2_E', 'SEC2_F'],
            ['Col1', 'Col5', 'Col6'],
            ['val1', 'val5', 'val6'],
            ['val1', 'val5', 'val6'],
            ['val1', 'val5', 'val6']]
        target_file = self.make_fake_csv(empty_list)
        filewriter = csv.writer(target_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL, lineterminator='\n')
        for row in test1_target:
                filewriter.writerow(row)

        self.assertEqual(
            write_csv_file.getvalue(),
            target_file.getvalue())

        # Test 3 attempt
        write_csv_file = self.make_fake_csv(empty_list)
        spread_sheet.select_population_data(write_csv_file, 'sec1')

        # Test 3 target
        test1_target = [
            ['SEC1_B', 'SEC1_C', 'SEC1_D'],
            ['Col2', 'Col3', 'Col4'],
            ['val2', 'val3', 'val4'],
            ['val2', 'val3', 'val4'],
            ['val2', 'val3', 'val4']]
        target_file = self.make_fake_csv(empty_list)
        filewriter = csv.writer(target_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL, lineterminator='\n')
        for row in test1_target:
                filewriter.writerow(row)

        self.assertEqual(
            write_csv_file.getvalue(),
            target_file.getvalue())

    def test_write_table(self):

        # not testing built-in csv function
        pass

if __name__ == '__main__':
    unittest.main()
