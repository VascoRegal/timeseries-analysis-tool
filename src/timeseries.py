import numpy as np

from database import fetch_records
from utils import calculate_metrics, calculate_tests, autocorrelate
from plotting import *

COMMON_WINDOW_NAME = "TIME SERIES"

class SeriesGroup:
    def __init__(self, glbls, name, opts):
        time_int = glbls['timeInterval']
        if opts.get('plot'):
            plot = opts['plot']
        else:
            plot = glbls['plot']
        conn_str = glbls['connectString']

        valInt = opts['valuesIntervals']
        def_vals = valInt['default']
        valIntIndicators = [k for k in valInt.keys() if k != 'default']
        valIntData = {} 

        for i in valIntIndicators:
            valIntData[i] = self.calculate_bucket(valInt[i])

        self.begin = time_int['begin']
        self.end = time_int['end']
        self.plot = plot
        self.conn_str = conn_str 
        self.name = name
        self.query = opts['query']
        self.ctx = opts['context']
        self.indicators = opts['indicators']
        self.timestamp = opts['timestamp']
        self.separatePlots = opts['separatePlots']
        self.valIntData = valIntData
        self.metrics = opts['metrics']
        self.tests = opts['test']
        self.casuality = opts['causality']

        self.timeseries = []

        self.process()

    def calculate_bucket(self, lst):
        return np.arange(lst['from'], lst['to'], lst['interval'])


    def process(self):
        data = {}
        records = fetch_records(self.conn_str, self.query)

        for r in records:
            ctx_dict = {}
            key = []
            stamp = r[self.timestamp]
            for c in self.ctx:
                key.append(r[c])
                ctx_dict[c] = r[c]
            keystr = '/'.join(map(str,key))

            for i in self.indicators:
                if keystr not in data.keys():
                    data[keystr] = {
                        'context':ctx_dict,
                        'vals': {}
                    }

                
                else:
                    if i not in data[keystr]['vals'].keys():
                        data[keystr]['vals'][i] = {stamp : r[i]}
                    else:
                        data[keystr]['vals'][i][stamp] = r[i]
            
        for d in data.keys():
            for i in data[d]['vals'].keys():
                self.timeseries.append(TimeSeries(self.name, d, i, data[d]))


    def visit_series(self, print=False):
        for ts in self.timeseries:
            ts.visit(self.metrics, self.tests)

            if self.plot:
                ts.plot(sep=self.separatePlots)

            if ts.indicator in self.valIntData.keys():
                ts.histogram(self.valIntData[ts.indicator])


            ts.show()

        show_plots()




class TimeSeries:
    def __init__(self, grp, id, indicator , values):
        self.group = grp
        self.id = id
        self.indicator = indicator
        self.ctx = values['context']
        self.vals = values['vals'][indicator]

        self.metrics = None
        self.tests = None

    
    def visit(self, metrics, tests):
        self.get_metrics(metrics)
        self.get_tests(tests)

    def plot(self, sep):
        opts = {"label":f"{self.id} - {self.indicator}",
                "marker": "o"}

        if sep:
            window = COMMON_WINDOW_NAME + f"{self.id} - {self.indicator} [{self.group}]"
        else:
            window = COMMON_WINDOW_NAME + f"[{self.group}]"
    
        gen_plot(list(self.vals.keys()), list(self.vals.values()),
                "time", self.indicator, f"{self.id} - {self.indicator}",
                window, **opts)

    def histogram(self, buckets):
        opts = {"bins" : buckets,
                "label": f"{self.id} - {self.indicator}"}

        gen_hist(list(self.vals.values()), self.indicator, "Number Of Samples",
                 f"{self.id} - {self.indicator} Absolute Distribution",
                 f"Sample Distribution - {self.indicator} [{self.group}]", **opts)

    
    def get_metrics(self, metrics):
        self.metrics = calculate_metrics(metrics, list(self.vals.values()))

    def get_tests(self, tests):
        self.tests = calculate_tests(tests, list(self.vals.keys()), list(self.vals.values()))

    def show(self):
        print("*"*50)
        print("|_ CONTEXT")
        for c in self.ctx.keys():
            print(f"\t{c} : {self.ctx[c]}")

        print("|_ INDICATOR")
        print(f"\t{self.indicator}")

        print("|_ METRICS")
        for m in self.metrics.keys():
            print(f"\t{m:12} : {self.metrics[m]}")

        print("|_ TESTS")
        for t in self.tests.keys():
            print(f"\t{t:12} : {self.tests[t]}")
        print("*"*50)
        print("\n")