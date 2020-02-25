# coding=utf8

import os
import re
import pandas as pd

number_pattern = re.compile('[+-]?([0-9]*[.])?[0-9]+')


if __name__ == '__main__':
    path = '../../data/geo/sql_data'
    terminals = set()
    for filename in os.listdir(path):
        table_name = filename.split('.')[0]
        filepath = os.path.join(path, filename)
        df = pd.read_csv(filepath)
        for column in df.columns:
            values = df[column].tolist()
            v = values[0]
            if number_pattern.match(str(v).strip()):
                # number
                for i in values:
                    if '.' in str(i):
                        # float
                        terminals.add('"%s"' % str(float(i)))
                    else:
                        terminals.add('"%s"' % str(int(i)))
            else:
                # str
                for i in values:
                    i = i.strip()
                    terminals.add('"%s"' % i)
    print(terminals)