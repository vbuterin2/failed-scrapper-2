import pandas as pd
import collections


class TableParser:
    @staticmethod
    def read_html(table_html):
        return pd.read_html(table_html, thousands=None, encoding="UTF-8")

    @staticmethod
    def recur_dictify(frame):
        if len(frame.columns) == 1:
            if frame.values.size == 1: return frame.values[0][0]
            return frame.values.squeeze()
        grouped = frame.groupby(frame.columns[0])
        d = {k: TableParser.recur_dictify(g.iloc[:, 1:]) for k, g in grouped}
        return d

    @staticmethod
    def flatten(d, parent_key='', sep=' '):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(TableParser.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
