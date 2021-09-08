from parsers import FileParser
from database import fetch_records
from plotting import *
from utils import calculate_bucket, TIME_CONVERSION_TABLE, calculate_metrics, calculate_tests, test_causality

from datetime import datetime
import sys

def main():
    if len(sys.argv) != 2:
        exit("File not provided")
    
    parser = FileParser()
    groups = []

    config = parser.parse(sys.argv[1])

    if config is None:
        exit("Invalid file format")

    global_vals = config['global']
    start = global_vals['timeInterval']['begin']
    end = global_vals['timeInterval']['end']
    plot = global_vals['plot']
    timeseries = config['timeseries']

    for g, conf in timeseries.items():
        print("*"*60)
        print(f"GROUP : {g}")
        data = {}
        records = fetch_records(global_vals['connectString'], conf['query'])

        if 'plot' in conf.keys():
            plot = conf['plot']


        '''
        processa o dicionário retornado pela query numa estrutura do tipo:

        'key': {
            'context': {
                ctx_field1: ctx_val1,
                ctx_field2: ctx_val2,
                ...
            },

            'vals': {
                indicator1 : {
                    timestamp1: indicator1_val1,
                    timestamp2: indicator1_val2,
                    ...
                },

                indicator2 : {
                    timestamp1: indicator2_val1,
                    ...
                }
            }

        }

        em que key é a string de concatenação dos contextos

        '''
        for r in records:
            ctx_dict = {}
            key=[]
            
            for c in conf['context']:
                ctx_dict[c] = r[c]
                key.append(r[c])
            
            keystr = '/'.join(map(str,key))

            stamp = r[conf['timestamp']]

            for i in conf['indicators']:
                if keystr not in data.keys():
                    data[keystr] = {
                        'context': ctx_dict,
                        'vals': {}
                    }

                else:
                    if i not in data[keystr]['vals'].keys():
                        data[keystr]['vals'][i] = { stamp : r[i] }
                    else:
                        data[keystr]['vals'][i][stamp] = r[i]

        

        '''

        itera a estrutura criada anteriormente e analisa os datasets de cada entrada

        '''
        for context, info in data.items():

            print(f"\t|_ CONTEXT")
            for c,d in info['context'].items():
                print(f"\t\t{c} : {d}")
            print("\t|_ SERIES")

            for i,v in info['vals'].items():

                print("\t\t|_ INDICATOR")
                print(f"\t\t\t{i}")


                #plotting 
                if plot:
                    opts = {"label":f"{context} - {i}",
                            "marker": "o"}

                    if conf['separatePlots']:
                        window = f"TIME SERIES - {context} [{g}]"
                    else:
                        window = f"TIME SERIES [{g}]"

                    gen_plot(list(v.keys()), list(v.values()), 'date', 'indicator',
                            f"context: {context} from {start} to {end}",
                            window, **opts)



                #histograma de intervalo de valores
                if i in conf['valuesIntervals'].keys():
                    bins = conf['valuesIntervals'][i]
                else:
                    bins = conf['valuesIntervals']['default']

                bins = calculate_bucket(bins)
                opts = {"label": f"{context} - {i}"}
                gen_hist(list(v.values()), bins, i, 'Number of Samples',
                        f'[context:{context}] {i} Values Interval',
                        f'VALUES INTERVAL - {i} [{g}]',**opts)


                #histograma de intervalo de tempo
                if i in conf['timeIntervals'].keys():
                    bins = conf['timeIntervals'][i]
                else:
                    bins = conf['timeIntervals']['default']

                bins = calculate_bucket(bins)

                ts = [datetime.timestamp(x) for x in v.keys()]
                count = []

                for cnt in range(0, len(ts)):
                    if cnt + 1 == len(ts):
                        break
                    else:
                        count.append(ts[cnt+1] - ts[cnt])

                gen_hist([x / TIME_CONVERSION_TABLE[conf['timeIntervalsUnit']]for x in count],
                         bins, f'time ({conf["timeIntervalsUnit"]})', 'Number of Samples',
                        f'[context:{context}] {i} Time Interval', f'TIME INTERVAL - {i} [{g}]',
                        **opts)

                #calculo das metricas
                print("\t\t|_ METRICS")
                for metric, val in calculate_metrics(conf['metrics'], list(v.values())).items():
                    print(f"\t\t\t{metric:12} : {val}")

                #calculo dos testes
                print("\t\t|_ TESTS")
                for test, val in calculate_tests(conf['test'], list(v.keys()), list(v.values())).items():
                    print(f"\t\t\t{test:12} : {val}")

                print("\n")


            #causalidade
            print("\t|_ CAUSALITY (PEARSON CORRELATION)")
            for lst in conf['causality']:
                args=[]
                for ind in lst:
                    args.append(list(info["vals"][ind].values()))
                print(f"\t\t{'-'.join(map(str,lst))} : {test_causality(args[0], args[1])}")
            


        print("*"*60)
        print("\n")
        show_plots()


if __name__ == '__main__':
    main()