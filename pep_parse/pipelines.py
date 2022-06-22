import collections
import csv
import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    """Pipeline формирует таблицу из статусов PEP
    в формате "Статус" - "Количество"
    и подсчитывает общее количество документов.
    Возврат осуществляется в виде status_summary_date.csv
    по пути /results/pep_date.csv
    """
    pep_sum = collections.defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        status = item['status']
        self.pep_sum[status] += 1
        return item

    def close_spider(self, spider):
        dir_path = BASE_DIR / 'results'
        dir_path.mkdir(exist_ok=True)
        now = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'status_summary_{now}.csv'
        file_path = dir_path / file_name
        results = ['Статус,Количество']
        with open(file_path, mode='w', encoding='utf-8') as f:
            csv_writer = csv.writer(f,
                                    dialect='unix')
            total = sum(self.pep_sum.values())
            csv_writer.writerows([
                results,
                *self.pep_sum.items(),
                ['Total', total]
            ])
