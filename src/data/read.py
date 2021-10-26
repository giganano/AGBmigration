
from ..utils import logplus12_bracket_conversion, logNO_bracket_conversion
import astropy.table as table
from astropy.io import fits
import numpy as np
import pickle
import vice
import os
PATHROOT = os.path.abspath(os.path.dirname(__file__))


def read(which):
	r"""
	Read in a given sample.

	Parameters
	----------
	which : ``str``
		A keyword denoting which sample to pull.

			- "pilyugin2010" : Pilyugen, Vilchez & Thuan (2010) [1]_
			- "berg2012" : Berg et al. (2012) [2]_
			- "izotov2012" : Izotov, Thuan & Guseva (2012) [3]_
			- "james2015" : James et al. (2015) [4]_
			- "dopita2016" : Dopita, Kewley, Sutherland & Nicholls (2016) [5]_
			- "belfiore2017" : Belfiore et al. (2017) [6]_
			- "schaefer2020" : Schaefer et al. (2020) [7]_
			- "vincenzo2021" : Vincenzo et al. (2021) [8]_

	.. [1] Pilyugin, Vilchez & Thuan (2010), ApJ, 720, 1738
	.. [2] Berg et al. (2012), ApJ, 754, 98
	.. [3] Izotov, Thuan & Guseva (2012), A&A, 546, A122
	.. [4] James et al. (2015), MNRAS, 448, 2687
	.. [5] Dopita, Kewley, Sutherland & Nicholls (2016), Ap&SS, 361, 61
	.. [6] Belfiore et al. (2017), MNRAS, 469, 151
	.. [7] Schaefer et al. (2020), ApJ, 890, 3
	.. [8] Vincenzo et al. (2021), arxiv:2106.03912
	""" 
	return {
		"pilyugin2010": 	pilyugin2010,
		"berg2012": 		berg2012,
		"izotov2012": 		izotov2012,
		"james2015": 		james2015,
		"dopita2016": 		dopita2016,
		"belfiore2017": 	belfiore2017,
		"schaefer2020": 	schaefer2020,
		"vincenzo2021": 	vincenzo2021,
		"chaos":			chaos_reader
	}[which.lower()]()


def berg2012(): 
	r""" 
	Reads the Berg et al. (2012) [1]_ data. 

	.. [1] Berg et al. (2012), ApJ, 754, 98 
	""" 
	return _blue_dwarf_reader(
		"%s/pilyugin-and-blue-dwarfs/dati_blue_dwarf/berg2012.dat" % (
			PATHROOT)) 


def izotov2012(): 
	r""" 
	Reads the Izotov, Thuan & Guseva (2012) [1]_ data. 

	.. [1] Izotov, Thuan & Guseva (2012), A&A, 546, A122 
	""" 
	return _blue_dwarf_reader(
		"%s/pilyugin-and-blue-dwarfs/dati_blue_dwarf/izotov2012.dat" % (
			PATHROOT)) 


def james2015(): 
	r""" 
	Reads the James et al. (2015) [1]_ data. 

	.. [1] James et al. (2015), MNRAS, 448, 2687 
	""" 
	return _blue_dwarf_reader(
		"%s/pilyugin-and-blue-dwarfs/dati_blue_dwarf/james2015.dat" % (
			PATHROOT)) 


def _blue_dwarf_reader(path): 
	r""" 
	Reads the data from one of the pilyugin subsets, all of which have the 
	same format. 
	""" 
	raw = np.genfromtxt(path) 
	return vice.dataframe({
		"[o/h]": 		[logplus12_bracket_conversion(row[0]) for row in raw], 
		"err_[o/h]": 	[row[1] for row in raw], 
		"[n/o]": 		[logNO_bracket_conversion(row[2]) for row in raw], 
		"err_[n/o]": 	[row[3] for row in raw] 
		})


def belfiore2017(): 
	r""" 
	Reads the MaNGA sample from Belfiore et al. (2017) [1]_. 

	.. [1] Belfiore et al. (2017), MNRAS, 469, 151 
	""" 
	raw = table.Table.read("%s/n_o_grad-manga.dat" % (PATHROOT), 
		format = "ascii") 
	oh = raw["10.50-10.75 12+log(O/H)"].data.tolist() 
	oh += raw["10.75-11.00 12+log(O/H)"].data.tolist() 
	oh = [logplus12_bracket_conversion(_) for _ in oh] 
	err_oh = raw["10.50-10.75 error 12+log(O/H)"].data.tolist() 
	err_oh += raw["10.75-11.00 error 12+log(O/H)"].data.tolist() 
	no = raw["10.50-10.75 log(N/O)"].data.tolist() 
	no += raw["10.75-11.00 log(N/O)"].data.tolist() 
	no = [logNO_bracket_conversion(_) for _ in no] 
	err_no = raw["10.50-10.75 error log(N/O)"].data.tolist() 
	err_no += raw["10.75-11.00 error log(N/O)"].data.tolist() 
	return vice.dataframe({
		"[o/h]": oh, 
		"err_[o/h]": err_oh, 
		"[n/o]": no, 
		"err_[n/o]": err_no 
		})


def pilyugin2010(): 
	r""" 
	Reads the data from Pilyugin, Vilchez & Thuan (2010) [1]_. 

	.. [1] Pilyugin, Vilchez & Thuan (2010), ApJ, 720, 1738 
	""" 
	raw = np.genfromtxt(
		"%s/pilyugin-and-blue-dwarfs/data_pilyugin/OHons-NOons.dat" % (
			PATHROOT)) 
	return vice.dataframe({
		"[o/h]": 		[logplus12_bracket_conversion(row[0]) for row in raw], 
		"err_[o/h]": 	len(raw) * [float("nan")], 
		"[n/o]": 		[logNO_bracket_conversion(row[1]) for row in raw], 
		"err_[n/o]": 	len(raw) * [float("nan")] 
		}) 


def dopita2016(): 
	r""" 
	Reads the data from Dopita et al. (2016) [1]_. 

	.. [1] Dopita, Kewley, Sutherland & Nicholls (2016), Ap&SS, 361, 61 
	""" 
	raw = np.genfromtxt("%s/dopita2016.dat" % (PATHROOT)) 
	return vice.dataframe({
		"[o/h]": 		[logplus12_bracket_conversion(row[0]) for row in raw], 
		"err_[o/h]": 	len(raw) * [float("nan")], 
		"[n/o]": 		[logNO_bracket_conversion(row[1]) for row in raw], 
		"err_[n/o]": 	len(raw) * [float("nan")] 
		}) 


def vincenzo2021(): 
	r""" 
	Reads the data from Vincenzo et al. (2021) [1]_. 

	.. [1] Vincenzo et al. (2021), arxiv:2016.03912 
	""" 
	f = open("%s/CNOdredgeup.obj" % (PATHROOT), "rb") 
	raw = pickle.load(f, encoding = "bytes") 
	f.close() 
	mgfe = raw[1].tolist() 
	feh = raw[2].tolist() 
	cfe = raw[3].tolist() 
	nfe = raw[4].tolist() 
	ch = raw[5].tolist() 
	nh = raw[6].tolist() 
	age = raw[7].tolist() 
	cn = raw[9].tolist() 
	no = [logNO_bracket_conversion(_) for _ in raw[11]] 
	oh = [a - b for a, b in zip(nh, no)] 
	data = vice.dataframe({
		"[mg/fe]": mgfe, 
		"[fe/h]": feh, 
		"[c/fe]": cfe, 
		"[n/fe]": nfe, 
		"[c/h]": ch, 
		"[n/h]": nh, 
		"age": age, 
		"[c/n]": cn, 
		"[o/h]": oh, 
		"[n/o]": no 
	}) 
	return data.filter(
		"[o/h]", ">=", -10).filter(
		"[o/h]", "<=", 10).filter(
		"[n/o]", ">=", -10).filter(
		"[n/o]", "<=", 10) 


def schaefer2020(): 
	r""" 
	Reads the data from Schaefer et al. (2020) [1]_ 

	.. [1] Schaefer et al. (2020), ApJ, 890, 3 
	""" 
	raw = fits.open("%s/Schaefer2020_spaxel_data.fits" % (PATHROOT))[1].data 
	return vice.dataframe({
		"[o/h]": [logplus12_bracket_conversion(_) for _ in raw["r23_met"]], 
		"err_[o/h]": [logplus12_bracket_conversion(_) for _ in 
			raw["r23_met_err"]], 
		"[n/o]": [logNO_bracket_conversion(_) for _ in raw["n_o"]], 
		"err_[n/o]": [logNO_bracket_conversion(_) for _ in raw["n_o_err"]], 
		"logmstar": raw["all_totmass"], 
		"manga_plate_id": raw["plateifu"] 
	}) 


def chaos_reader():
	r"""
	Reads in the data for the first six CHAOS galaxies (Berg et al. 2020 [1]_;
	Skillman et al. 2020 [2]_; Rogers et al. 2021 [3]_)

	.. [1] Berg et al. (2020), ApJ, 893, 96
	.. [2] Skillman et al. (2020), ApJ, 894, 138
	.. [3] Rogers et al. (2021), ApJ, 915, 21
	"""
	oh = []
	no = []
	files = ["chaos_ngc3184.dat", "chaos_ngc2403.dat"]
	for item in files:
		with open("%s/%s" % (PATHROOT, item), 'r') as f:
			while True:
				line = f.readline()
				if line == "": break
				if line[0] == '#': continue
				line = [float(_) for _ in line.split()]
				oh.append(line[0])
				no.append(line[2])
			f.close()
	with open("%s/chaos_m101.dat" % (PATHROOT), 'r') as f:
		while True:
			if line == "": break
			if line[0] == '#': continue
			line = line.split()
			oh.append(float(line[1]))
			co = float(line[3])
			cn = float(line[5])
			no.append(co - cn)
		f.close()
	files = ["chaos_ngc628.dat", "chaos_ngc5194.dat", "chaos_ngc5457.dat"]
	for item in files:
		with open("%s/%s" % (PATHROOT, item), 'r') as f:
			while True:
				line = f.readline()
				if line == "": break
				if line[0] == '#': continue
				line = line.split()
				oh.append(float(line[1]))
				no.append(float(line[3]))
			f.close()
	return vice.dataframe({
		"[o/h]": [logplus12_bracket_conversion(_) for _ in oh],
		"[n/o]": [logNO_bracket_conversion(_) for _ in no]
	})

