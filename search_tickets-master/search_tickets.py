# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable

class TrainCollection:  
    # 列车车次信息列表项序列
    TRAIN_NO = 2
    STARTING_STATION = 3
    TERMINAL_STATION = 4
    FROM_STATION = 5
    TO_STATION = 6
    START_TIME = 7
    ARRIVE_TIME = 8
    DURATION = 9
    TICKET_LEFT = 10
    TICKET_DATE = 12
    HIGH_GRADE_SOFT_BERTH = 20
    SOFT_BERTH = 22
    SOFT_SEAT = 23
    STANDING_TICKET = 25
    HARD_BERTH = 27
    HARD_SEAT = 28
    SECOND_CLASS_SEAT = 29
    FIRST_CLASS_SEAT = 30
    SPECIAL_CLASS_SEAT = 31
    CRH_BERTH = 32
    
    header = '车次 始发站 终点站 出发站 到达站 出发时间 到达时间 历时 商务座特等座 一等座 二等座 高级软卧 软卧 硬卧 动卧 软座 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, original_duration):
        duration = original_duration.replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_list = raw_train.partition('|')[2].split('|')
            train_no = raw_train_list[self.TRAIN_NO]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    raw_train_list[self.STARTING_STATION],
                    raw_train_list[self.TERMINAL_STATION],
                    raw_train_list[self.FROM_STATION],
                    raw_train_list[self.TO_STATION],
                    raw_train_list[self.START_TIME],
                    raw_train_list[self.ARRIVE_TIME],
                    self._get_duration(raw_train_list[self.DURATION]),
                    raw_train_list[self.SPECIAL_CLASS_SEAT],
                    raw_train_list[self.FIRST_CLASS_SEAT],
                    raw_train_list[self.SECOND_CLASS_SEAT],
                    raw_train_list[self.HIGH_GRADE_SOFT_BERTH],
                    raw_train_list[self.SOFT_BERTH],
                    raw_train_list[self.HARD_BERTH],
                    raw_train_list[self.CRH_BERTH],
                    raw_train_list[self.SOFT_SEAT],
                    raw_train_list[self.HARD_SEAT],
                    raw_train_list[self.STANDING_TICKET]
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        #将站点的英文缩写转换为中文输出
        for train in self.trains:
            for i in range(1,5):
                train[i] = list(stations.keys())[list(stations.values()).index(train[i])]
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'.format(       
        train_date=date, from_station=from_station, to_station=to_station
    )
    # 获取参数
    options = ''.join([key for key, value in arguments.items() if value is True])
    
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    # 获取列车车次列表
    available_trains = r.json()['data']['result']
    TrainCollection(available_trains,options).pretty_print()

if __name__ == '__main__':
    cli()