from typing import Optional, Tuple, Any, List

from numpy import nan        
import pandas as pd
from pandas import DataFrame

from ..schemas.exercise import Exercise, InSet

sets = ['1 подход', '2 подход', '3 подход','4 подход', '5 подход']
columns = ['Неделя', 'Тренировка', 'Мышечные группы', 'Упражнения', 'Количество подходов/повторений', 'Рабочий вес', 'Комментарии', 'Отдых между подходами', *sets]


def current_training(df, week: int, tr: int):
    data = df[
        (df['Неделя'] == week) & (df['Тренировка'] == tr)
    ].loc[:, columns]
    data.index = range(1, data.shape[0] + 1)
    data[sets] = data[sets].fillna(0)
    return data


def max_column_value(df, column: str = 'Неделя'):
    return max([i for i in df[column] if isinstance(i, int)])


def training_list_coordinates(df: DataFrame):
    num_week = max_column_value(df, 'Неделя')
    num_traning = max_column_value(df, 'Тренировка')
    coordinates = []
    for w in range(1, num_week + 1):
        for t in range(1, num_traning + 1):
            xy = df[(df['Неделя'] == w) & (df['Тренировка'] == t)]
            coordinates.append([xy.index[0], xy.index[-1] + 1])
    return coordinates

def training_list(df: DataFrame):
    coordinates_list = training_list_coordinates(df)
    result = []
    for c in coordinates_list:
        data = df[columns].iloc[c[0]:c[1]]
        data[sets] = data[sets].fillna(0)
        data.index = range(1, data.shape[0] +1)
        result.append(data)
    return result


class DataFrameManager:
    def __init__(
        self,
        path='/home/vasiliy/code/gym-back/gym_api/files/01_2025.xlsx',
    ):
        self.dataframe_path = path
        self.read_dataframe()
        self.validate_dataframe()
        
    def save_dataframe(self, path: Optional[str] = None):
        p = path or self.dataframe_path
        self.df.to_excel(p)
        
    def read_dataframe(self, path: Optional[str] = None):
        p = path or self.dataframe_path
        self.df: DataFrame = pd.read_excel(p)
        self.df.iloc[:, 0:5] = self.df.iloc[:, 0:5].ffill(axis=0)
    
    def _calculate_cell_coordinates(
        self,
        week: int, tr: int, st: int, ex: int
    ) -> Tuple[int, str]:
        row = self.df[
            (self.df['Неделя'] == week) & (self.df['Тренировка'] == tr)
        ].index[ex -1]
        col = 'GYM' if st == 'GYM' else f"{st} подход"
        return row, col 
    
    def _update_cell(self, row: int, col: str, value: Any):
        self.df.loc[row, col] = value    
    
    def current_tarin(self, week: int, day: int) -> List:
        df = current_training(self.df, week, day)
        # df['GYM'] = df['GYM'].replace(nan, '-')
        exercises = []
        for idx, row in df.iterrows():
            sts = list(row[sets])
            ex = Exercise(
                week=row['Неделя'],
                day=row['Тренировка'],
                muscles=str(row['Мышечные группы']),
                desc=str(row['Комментарии']),
                exercise=row['Упражнения'],
                weight=str(row['Рабочий вес']),
                rest=str(row['Отдых между подходами']),
                repeats=str(row['Количество подходов/повторений']),
                sets=[
                    InSet(numField=i, value=sts[i]) for i in range(len(sts))
                ],
                exerciseIdx=idx
            )
            exercises.append(ex.model_dump())
        return exercises
            

    def update(self, week: int, tr: int, st: int, ex: int, value: Any):
        row, col = self._calculate_cell_coordinates(week, tr, st, ex)
        self._update_cell(row, col, value)

    def validate_dataframe(self):
        if 'GYM' not in self.df.columns:
            self.df['GYM'] = nan
            
    def history(self)-> List:
        '''все тренировки из файла'''
        exercises: List = []
        trainings = training_list(self.df)
        for data in trainings:
            for idx, row in data.iterrows():
                ex = Exercise(
                    week=row['Неделя'],
                    day=row['Тренировка'],
                    muscles=str(row['Мышечные группы']),
                    desc=str(row['Комментарии']),
                    exercise=row['Упражнения'],
                    weight=str(row['Рабочий вес']),
                    rest=str(row['Отдых между подходами']),
                    sets=list(row[sets]),
                    exerciseIdx=idx
                )
                exercises.append(ex)
        return exercises
                
            
        
        
