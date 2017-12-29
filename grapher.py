from altair import *
import pandas as pd

data = pd.read_csv('modules.csv', delimiter=',')
print(data)

Chart(data).mark_bar().encode(
	x=X('Mark',
		bin=Bin(
			maxbins = 10.0,
			),
		),
	)