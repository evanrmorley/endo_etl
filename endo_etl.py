import csv
import sys
import re

def find_in_str(str, lst):
    #import pdb; pdb.set_trace()
    match = re.search('(.+?) \((.+?)\)', str)
    if match is None:
        raise ValueError
    value = match.group(1)
    key = match.group(2)
    if key in lst:
        return key, value
    else:
        raise ValueError
    '''
    key = re.search('(.+?) \((.+?)\)', str).group(2)
    for item in lst:
        try:
            key_index = str_list.index('({})'.format(item))
            return re.search('\((.+?)\)', str_list[key_index]).group(1), str_list[key_index-1]  #re.search to get rid of key parenthesis
        except ValueError:
            continue
    raise ValueError
    '''

def replace_unprintable_with_space(s):
    return re.sub(r'[^\x20-\x7E]+',' ', s)

def convert(file_input, file_output, *column_names):
    #import pdb; pdb.set_trace()
    table = []
    with open(file_input, 'rb') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        index_last_row = -1
        for row in dataReader:
            if row[0] == column_names[0]:
                table.append(["" for x in range(len(column_names))])
            try:
                index_last_row = column_names.index(row[0])
                table[-1][index_last_row] = replace_unprintable_with_space(row[1])
            except ValueError:
                try:
                    key, value = find_in_str(replace_unprintable_with_space(row[1]), column_names)
                    index_key = column_names.index(key)
                    table[-1][index_key] = '{} {}'.format(value, table[-1][index_key]).strip()
                    index_last_row = -1
                except ValueError:
                    if row[0] == '' and row[1] != '' and index_last_row > -1:
                        table[-1][index_last_row] = '{}; {}'.format(table[-1][index_last_row], replace_unprintable_with_space(row[1]))
                    elif row[0] != '' and index_last_row > -1:
                        index_last_row = -1
                    else:
                        continue

    print("length of table with duplicates: {}".format(len(table)))
    #remove duplicate rows trom table
    table = [list(x) for x in set(tuple(l) for l in table)]
    print("length of table without duplicates: {}".format(len(table)))

    '''
    for row in table:
        if 'Diamond' in row[0]:
            print row
    '''


    with open(file_output, 'wb') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',  quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in table:
            datawriter.writerow(row)

def main():
    if (len(sys.argv) == 2 and sys.argv[1] == "--help") or len(sys.argv) < 4:
        print("Usage: python {} [--help] filename_in filename_out column_name1 [column_name...]".format(sys.argv[0]))
    else:
        convert(*sys.argv[1:])

if __name__ == "__main__":
    main()