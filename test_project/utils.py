import json
import numpy as np
import pandas as pd
import requests as re
import seaborn as sns
import matplotlib.pyplot as plt

from test_project.config import def_figsize

from typing import NoReturn, List, Union


class Data:
    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df

    @classmethod
    def read_json_url(cls, path: str) -> 'Data':
        r = re.get(path)
        return cls(pd.DataFrame(r.json()))

    @classmethod
    def read_csv(cls, path: str) -> 'Data':
        return cls(pd.read_csv(path, index_col=0))

    @classmethod
    def read_json(cls, path: str) -> 'Data':
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(pd.DataFrame(data))


class Plots:
    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df

    def plot_columns(self,
                     columns: List[str],
                     type_: str = 'plot',  # or scatter
                     *args, **kwargs) -> Union[NoReturn, str]:
        plt.figure(figsize=def_figsize)
        for column in columns:
            if self.__check_is_numeric(self.df[column]):
                getattr(plt, type_)(self.df.index, self.df[column].values, label=column)
                plt.title('Column plot')
                plt.xlabel('df index')
                plt.legend(loc='best')
        return self.__end_plot_method(plt, *args, **kwargs)

    def plot_pairplot(self, *args, **kwargs) -> NoReturn:
        sns.pairplot(self.df)
        return self.__end_plot_method(plt, *args, **kwargs)

    def plot_corr_heatmap(self, *args, **kwargs) -> Union[NoReturn, str]:
        c = self.df.corr(numeric_only=True)
        sns.heatmap(c, annot=True, fmt='.2f',)
        return self.__end_plot_method(plt, *args, **kwargs)

    def plot_unique(self, column: str, *args, **kwargs) -> Union[NoReturn, str]:
        if self.__check_is_numeric(self.df[column]):
            sns.histplot(data=self.df, x=column)
            plt.title(f'Unique {column} values')
            plt.xlabel('Unique values')
            plt.ylabel('Count')
            return self.__end_plot_method(plt, *args, **kwargs)

    def count_compare_unique(self,
                             unique_column: str,
                             compare_column: str,
                             compare_type: str = 'mean',  # min, max, sum, std, etc
                             *args, **kwargs
                             ) -> Union[NoReturn, str]:
        unique_values = self.df[unique_column].unique()
        results = []
        for value in unique_values:
            dff = self.df[self.df[unique_column] == value]
            results.append(getattr(np, compare_type)(dff[compare_column]))

        plt.title(f'{compare_type} {compare_column} value for {unique_column} groups')
        plt.bar(unique_values, results)
        return self.__end_plot_method(plt, *args, **kwargs)

    def boxplot(self, unique_column: str, count_column: str, *args, **kwargs) -> Union[NoReturn, str]:
        sns.boxplot(data=self.df, x=unique_column, y=count_column)
        return self.__end_plot_method(plt, *args, **kwargs)

    @staticmethod
    def __end_plot_method(plt, show: bool = True, save_fn: str = '') -> Union[NoReturn, str]:
        plt.tight_layout()
        if show: plt.show()
        if save_fn != '':
            plt.savefig(save_fn)
            return save_fn
        return None

    @staticmethod
    def __check_is_numeric(column: pd.Series) -> bool:
        return True if np.issubdtype(column.dtype, np.number) else False
