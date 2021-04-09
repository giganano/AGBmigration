
from ..utils import logplus12_bracket_conversion, logNO_bracket_conversion 
import astropy.table as table 
import numpy as np 
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

			- "berg2012" : Berg et al. (2012) [1]_ 
			- "izotov2012" : Izotov, Thuan & Guseva (2012) [2]_ 
			- "james2015" : James et al. (2015) [3]_ 

	.. [1] Berg et al. (2012), ApJ, 754, 98 
	.. [2] Izotov, Thuan & Guseva (2012), A&A, 546, A122 
	.. [3] James et al. (2015), MNRAS, 448, 2687 
	""" 
	return {
		"pilyugin2010": 	pilyugin2010, 
		"berg2012": 		berg2012, 
		"izotov2012": 		izotov2012, 
		"james2015": 		james2015, 
		"dopita2016": 		dopita2016, 
		"belfiore2017": 	belfiore2017 
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

	.. [1] Pilyugez, Vilchez & Thuan (2010), ApJ, 720, 1738 
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















































