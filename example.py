import classifier as cl

path = './ephys/96711008.abf'
features = ['time_to_first_spike', 'burst_number', 'adaptation_index']

traces = cl.abf_to_traces(path)
etypes = cl.trace_classifier(traces, features)
print etypes

