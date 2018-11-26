#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a class to read csv and caculate stock datas'

__author__ = 'kevin deng'


import pandas as pd


# stock原始数据，保存为DataFrame格式
class StockOriginData(object):
    # 初始化需传入id字符串，沪深以SH、SZ开头
    def __init__(self, sid):
        self._sid = sid
        self.__read_stock_data(sid)

    def __read_stock_data(self, stock_id):
        # 读取负债表数据
        self._fzb = pd.read_csv(r'data/%s_fzb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._fzb, "报表日期")

        # 读取利润表数据
        self._lrb = pd.read_csv(r'data/%s_lrb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._lrb, "报表期截止日")

        # 读取流量表数据
        self._llb = pd.read_csv(r'data/%s_llb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._llb, "报表期截止日") 
        return

    @property
    def fzb(self):
        return self._fzb;
    @property
    def lrb(self):
        return self._lrb;
    @property
    def llb(self):
        return self._llb;


def add_report_time(data, index_name):
    list_time = []
    for i in data[index_name]:
        str_i = str(i)
        list_time.append(str_i[:4] + '-' + str_i[4:6] + '-' + str_i[6:8])
    # print(list_time)

    data['报告时间'] = [pd.to_datetime(t) for t in list_time]
    data.index = data['报告时间']
    return
    

# 提取和计算股票基本面参数，输入StockOriginData对象
class StockData(object):
    # 按类别提取数据，month 12月为年报数据，6月为半年报，3、9月为季报。
    def __init__(self, data, month):
        self._fzb = data.fzb[data.fzb.index.month == month]
        self._lrb = data.lrb[data.lrb.index.month == month]
        self._llb = data.llb[data.llb.index.month == month]

    def caculate(self):
        result = pd.DataFrame()

        # 负债表
        result['货币资金'] = self._fzb['货币资金']/1000000
        result['应收账款'] = self._fzb['应收账款']/1000000
        result['流动资产'] = self._fzb['流动资产合计']/1000000
        result['存货']     = self._fzb['存货']/1000000
        result['资产总计'] = self._fzb['资产总计']/1000000
        result['应付利息'] = self._fzb['应付利息']/1000000
        result['应付账款'] = self._fzb['应付账款']/1000000
        result['流动负债'] = self._fzb['流动负债合计']/1000000
        result['负债合计'] = self._fzb['负债合计']/1000000
        result['股东权益合计'] = self._fzb['所有者权益(或股东权益)合计']/1000000

        # 利润表
        result['营业总收入'] = self._lrb['营业总收入']/1000000
        result['营业收入']   = self._lrb['营业收入']/1000000
        result['营业总成本'] = self._lrb['营业总成本']/1000000
        result['营业成本']   = self._lrb['营业成本']/1000000
        result['销售费用']   = self._lrb['销售费用']/1000000    
        result['管理费用']   = self._lrb['管理费用']/1000000    
        result['财务费用']   = self._lrb['财务费用']/1000000    
        result['营业利润']   = self._lrb['营业利润']/1000000
        result['净利润']     = self._lrb['净利润']/1000000
        result['归母净利润'] = self._lrb['归属于母公司所有者的净利润']/1000000
        result['每股收益']   = self._lrb['基本每股收益']/1000000
        result['稀释每股收益'] = self._lrb['稀释每股收益']/1000000
          
        result['费用率'] = (result['销售费用']+result['管理费用']+result['财务费用']) / result['营业总收入']
        result['营业利润率'] = result['营业利润'] / result['营业收入']
        result['毛利润'] = result['营业收入'] - result['营业成本']
        result['毛利率'] = result['毛利润'] / result['营业收入']
        result['净利率'] = result['归母净利润'] / result['营业收入']
        
        # 流量表
        result['经营现金流入'] = self._llb['经营活动现金流入小计']/1000000        
        result['经营现金流出'] = self._llb['经营活动现金流出小计']/1000000        
        result['投资现金流入'] = self._llb['投资活动现金流入小计']/1000000        
        result['投资现金流出'] = self._llb['投资活动现金流出小计']/1000000        
        result['筹资现金流入'] = self._llb['筹资活动现金流入小计']/1000000        
        result['筹资现金流出'] = self._llb['筹资活动现金流出小计']/1000000        
        result['经营现金流量净额'] = self._llb['一、经营活动产生的现金流量净']/1000000
        result['投资现金流量净额'] = self._llb['二、投资活动产生的现金流量净']/1000000
        result['筹资现金流量净额'] = self._llb['三、筹资活动产生的现金流量净']/1000000
        result['期末现金等价余额'] = self._llb['六、期末现金及现金等价物余额']/1000000

        # 统计值

        result['负债率'] = result['负债合计']/result['资产总计']
        result['总资产周转率'] = result['营业收入']/result['资产总计']
        result['应收账款周转率'] = result['营业收入']/result['应收账款']
        result['应付账款周转率'] = result['营业收入']/result['应付账款']
        # 存货周转率=营业成本*2/（期初存货+期末存货）
        # 经营周期天数 = 存货周转天数+应收天数-应付天数
        result['净资产收益率'] = result['净利润']/result['股东权益合计']
        result['总资产收益率'] = result['净利润']/result['资产总计']
    
        # 流动比率＝流动资产/流动负债
        result['流动比率'] = result['流动资产']/result['流动负债']
        # 速动比率＝（流动资产-存货）/流动负债 
        result['速动比率'] = (result['流动资产']-result['存货'])/result['流动负债']
        # 获利含金量 = 经营活动现金流量/净利润
        result['获利含金量'] = result['经营现金流量净额']/result['净利润']

        result.index = self._fzb['报告时间']
        return result



# 读取股票数据，根据month筛选数据：month 12月为年报数据，6月为半年报，3、9月为季报。
def get_stock_data(sid, month):
    data = StockOriginData(sid)
    data_year = StockData(data, month)
    result = data_year.caculate()
    return result


if __name__=='__main__':
    data = get_stock_data("SH600519",12)
    print(data)
