from neo import io
import efel
import numpy

DELAY_THRESHOLD = 50 # ms
ADAPTATION_THRESHOLD = 0.05

efel.setThreshold(0)


def abf_to_traces(path):
	r = io.AxonIO(filename=path)
	bl = r.read_block(lazy=False, cascade=True)

	traces = []

	for segment in bl.segments:
		output_signal = segment.analogsignals[0]
		input_signal =  segment.analogsignals[1]

		offset = numpy.array(output_signal.t_start)*1000 # ms
		time = numpy.array(output_signal.times)*1000 # ms
		time = numpy.subtract(time, offset) # ms

		idx = input_signal.nonzero()[0][0]
		stim_start = time[idx]
		idx = input_signal.nonzero()[0][-1]
		stim_end = time[idx]

		voltage = numpy.array(output_signal)
		traces.append({'T': time, 'V':voltage,'stim_start': [stim_start], 'stim_end': [stim_end]})

	return traces


def trace_classifier(traces, features):
	etypes = []
	
	for trace in traces:
		etype = ""
		efel.reset()
		if efel.getFeatureValues([trace],['Spikecount'])[0]['Spikecount'][0] > 5:

			# efel.setDoubleSetting()
			feature_values = efel.getFeatureValues([trace],features)

			if has_delay(feature_values, DELAY_THRESHOLD):
				etype += 'd'
			elif has_burst(feature_values):
				etype += 'b'
			else:
				etype += 'c'

			if has_adaptation(feature_values):
				etype += 'AC'
			else:
				etype += 'NAC'

		etypes.append(etype)

	return etypes


def has_delay(feature_values, DELAY_THRESHOLD):
	return feature_values[0]['time_to_first_spike'] >= DELAY_THRESHOLD

def has_burst(feature_values):	
	return feature_values[0]['burst_number']

def has_adaptation(feature_values):
	return feature_values[0]['adaptation_index'] >= ADAPTATION_THRESHOLD

def cell_classifier():
	pass




