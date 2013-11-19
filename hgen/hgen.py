from string import uppercase
import csv


def num_to_new_base(num, radix):
    '''(int, int) -> list of int
    Convert a positive number num to its digit representation in base radix.
    Returns 0 when num is 0, not Null, for compatability purposes.

    >>>num_to_new_base(0, 26)
    [0]
    >>>num_to_new_base(1, 26)
    [1]
    >>>num_to_new_base(26, 26)
    [26]
    >>>num_to_new_base(27, 26)
    [1, 1]
    '''
    if num == 0:
        return [0]
    else:
        digits = []
        while num > 0:
            if num % radix == 0:
                digits.insert(0, radix)
                num = (num // radix) - 1
            else:
                digits.insert(0, num % radix)
                num = num // radix
        return digits


def base_num_to_num(digits, radix):
    '''(list of int, int) -> int
    Compute the numer given by digits in base radix.
    Returns 0 when digits is [0] for compatability purposes.

    >>>base_num_to_num([0], 26)
    0
    >>>base_num_to_num([1], 26)
    1
    >>>base_num_to_num([26], 26)
    26
    >>>base_num_to_num([1, 1], 26)
    27
    '''

    num = 0
    for d in digits:
        num = radix * num + d
    return num


def int2alpha(num):
    '''(int) -> str
    Converts a base10 integer num to an uppercase base26 alphabet string.
    '''

    if num == 0:
        return ''
    else:
        alphabet = {}
        for char in uppercase:
            alphabet[uppercase.find(char) + 1] = char

        ltr_list = []
        num_list = num_to_new_base(num, 26)
        count = len(num_list)
        for n in num_list:
            ltr_list.append(alphabet[n])
            count -= 1

        return ''.join(ltr_list)


def alpha2int(ltr):
    '''(str) -> int
    Converts an uppercase base26 alphabet string ltr to a base10 integer.
    '''

    alphabet = {}
    for char in uppercase:
        alphabet[char] = uppercase.find(char) + 1

    num_list = []
    count = len(ltr)
    for l in ltr.upper():
        num_list.append(alphabet[l])
        count -= 1

    return base_num_to_num(num_list, 26)


class SpreadSheet(object):
    '''
    Container for SpreadSheet objects.
    '''
    def __init__(self, fileobj):
        self.table = []
        self.headers = []

        filereader = csv.reader(fileobj, delimiter=',')
        for row in filereader:
            self.table.append(row)

    def create_headers(self, populations):
        '''(list  of lists of strings) -> None
        Populations is a list of lists that contain a section tag, starting
        column and ending column names expressed in base 26 alphabet
        characters, creates the span between the ranges, and creates this new
        list.
        '''

        self.headers = []

        for sub_population in populations:
            tag = sub_population[0].upper() + '_'
            start = alpha2int(sub_population[1])
            end = alpha2int(sub_population[2]) + 1

            for num in range(start, end):
                self.headers.append(tag + int2alpha(num))

    def lookup_header(self, ltr):
        '''(string) -> string
        Returns contents of header at location ltr.
        '''

        return self.headers[alpha2int(ltr) - 1]

    def lookup_data_point(self, column, row):
        '''(string, int) -> string
        Returns data at column and row.
        '''

        return self.table[row - 1][alpha2int(column) - 1]

    def select_population_data(self, targetfileobj, *sections):
        '''(fileobject, string[,]) -> None
        Isolates data from the table with headers containing
        only the selected sections. Writes to new targetfileobj.
        '''

        table_copy = list(self.table)
        table_copy.insert(0, self.headers)
        sections = [i.upper() for i in sections]
        pop_selections = []

        found_column = []
        for tag in sections:
            for column in table_copy[0]:
                trim_column = column.split('_')[0]
                if tag == trim_column:
                    found_column.append(table_copy[0].index(column))

        for row in table_copy:
            col_selection = []
            for column in found_column:
                col_selection.append(row[column])
            pop_selections.append(col_selection)

        filewriter = csv.writer(targetfileobj, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL, lineterminator='\n')
        for row in pop_selections:
            filewriter.writerow(row)

    def write_table(self, targetfileobj):
        '''(string) -> None
        Appends headers to table, then writes list
        lst to targetfile.
        '''

        table_copy = list(self.table)
        table_copy.insert(0, self.headers)

        filewriter = csv.writer(targetfileobj, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL, lineterminator='\n')
        for row in table_copy:
            filewriter.writerow(row)
