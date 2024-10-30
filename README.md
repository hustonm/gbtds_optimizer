# gbtds_optimizer

Tool for optimizing yields or metrics for the Roman Galactic Bulge
Time Domain Survey

This repository contains two tools for optimizing and evaluating the
field selection for the Roman Galactic Bulge Time Domain Survey:
- `gbtds_optimizer.py` is a general purpose optimizer that can take a
  map of survey yield for a single survey definition and provide
  contours yield for variations in pointing, exposure time and
  cadence.
- `results_plotter.py` is code to read in the results from
  `gbtds_optimizer.py` and plot/analyze it.
- `optimizeSlew.py` provides a tool to optimize and estimate slewing
  overheads in the GBTDS, and give a quick estimate of the impact of
  the field choice on the yield of bound Earth mass planets found via
  microlensing. 
  
  
## gbtds_optimizer.py

The basic inputs to this program are:
 - a yield map. This can be the yield defined however you like, but is
   probably something like the number of detections of something of
   interest, or the number of a certain type of target observed.
 - the exposure time and cadence that were used for calculating the
   yield map.
 - (optional) power law indexes describing how the yield changes when
   the exposure time and cadence are changed.
 - a field layout. This is a list of fixed and moveable fields that
   will be observed. The optimizer moves the moveable fields while
   keeping the fixed ones in place.
 - (default provided) slew and settle times as a function of slew angle.
 - (default provided) the detector layout.
 
 Full options can be found by running the code with the help flag
 i.e., `python gbtds_optimizer.py -h`
 
 An example of how to run the code for a chosen layout is
 ```
 python gbtds_optimizer.py fidu_mass6_rate.yield.csv 42.56 14.7315 \
        field_layouts/layout_7f_3_gal-center.centers \
        --alpha-cadence -0.406 --alpha-texp 0.616 \
		--lrange 2.2 -2.2 --brange -2.2 2.2 \
		--lstep 0.2 --bstep 0.2 \
		--cadence-bounds 7.0 15.0 \
		--nread-bounds 10 40 \
		--output-root fidu_mass6.layout_7f_3
 ```
 
 
## results_plotter.py

This will load an output pickle generated by `gbtds_optimizer.py` and
plot it, with various options. E.g., 


## optimizeSlew.py

The optimizeSlew.py script computes best path around a set of fields
fields and a rough scaling of microlensing planet detection
rates. Caution should be taken when increasing cadence beyond 15 minutes.

To run:

`python optimizeSlew.py <fields> <slew-times (short axis)> {<slew-times (diagonal)> <slew-times (long-axis)>`

The most up-to-date slew time file is
`slew_times_withResetReference_McEnery05232024.txt` - this file is the
`slew_times_McEnery05232024.txt` file provided by Julie McEnery with
6.12 seconds added to every slew to account for the reset read cycle
(3.08 s) and the first reference read that is subtracted from the ramp
(3.04 s). If you are using sample up the ramp signal to noise
estimates the reference read is already accounted for in the exposure
time, so you can remove it from the overheads. 

Fields files should have 3 columns with:
<Field_name> <l(deg)> <b(deg)>
