# DNA-HD error protection: analysis scripts

Python scripts used for the barcode statistics and channel-capacity calculations in:

> Earle, M. K.; Cronk, J. N.; Keyser, U. F.; Platnich, C. M. *Controlled Competition Reduces Errors in Nanostructure-Based DNA Data Storage.* (manuscript in preparation)

The paper introduces protector strands (toehold, mismatch and heat-activated clamp designs) that suppress 0-to-1 bit flips in DNA hard drive (DNA-HD) nanostructures read out by solid-state nanopore sensing. A single C–T mismatch protector gives >90% readout fidelity and a 25-fold increase in channel capacity over unprotected overhangs.

Upstream processing of the raw nanopore data (event extraction, peak finding and barcode assignment) was done with a separate package, [nas2](https://github.com/maxearle/nas2). The scripts here start from its outputs: pickled DataFrames of checked barcode assignments and HDF5 files of event current traces.

## Environment

Developed and run with **Python 3.12.2**. Required packages:

- numpy
- pandas
- matplotlib
- h5py (only for `plot_specific_barcodes.py`)

```bash
pip install numpy pandas matplotlib h5py
```

## Scripts

### `noisy_binary_channel_mutual_information.py`

Information-theoretic model of each protection scheme as an asymmetric noisy binary channel (Supporting Information, capacity section; paper Figure 6, Table 1 and Figure S4). Channel probabilities follow the convention *a* = P(1→1), *b* = P(1→0), *c* = P(0→1), *d* = P(0→0).

- `avg_mutual_inf_uniform_source(a, b, c, d)`: mutual information for a uniform source.
- `avg_mi_arb_p(a, b, c, d, px1)`: mutual information for an arbitrary prior P(X = 1); vectorised over `px1`.
- `find_capacity_and_p(a, b, c, d)`: capacity and capacity-achieving prior, found by scanning the prior over (0, 1) and taking the maximum mutual information.
- `capacity_and_capacity_achieving_p_with_err(b, berr, c, cerr)`: capacity and capacity-achieving prior from measured crossover rates, with asymmetric uncertainties obtained by recomputing at the high and low estimates of each rate and combining the deviations in quadrature.

Zero probabilities are replaced with a small epsilon to avoid log(0). The uniform-source function has a known singularity when a = c or b = d; offsetting one value by a small epsilon avoids it.

Running the file directly plots mutual information against prior for an example channel and prints its capacity.

### `barcode_counting_selected.py`

Counts barcode occurrence rates for the pooled-readout experiment with the 1 C–T mismatch protector (paper Figure 5). Four DNA-HDs written as 1000, 0100, 0010 and 0001 were pooled and read out together. The script plots the measured rates for a selected set of barcodes (0000, the four written barcodes, 0111 and 1111) with Wald-interval error bars, alongside the ideal 25% expected distribution.

### `barcode_counting_selected_test.py`

Variant of the above that plots all 16 possible 4-bit barcodes rather than the selected subset.

### `plot_specific_barcodes.py`

Plots a gallery of up to 15 nanopore translocation events assigned a chosen barcode (`bc_of_i`, default `0000`), with a 500 µs / 0.1 nA scale bar assuming 1 MHz sampling. The default inputs are from the 1 min mismatch-protector dataset. This was used for event-gallery figure panels such as the SI translocation gallery.

## Input data

Data file paths are hard-coded as absolute paths near the top of each script and need editing to run elsewhere:

- `barcode_counting_selected*.py` read a pickled DataFrame (`checked_protected.pkl`). The first column is the event name and the remaining columns are the per-bit assignments; rows containing NaN are skipped.
- `plot_specific_barcodes.py` reads a DataFrame in the same format and an `EVENTS.hdf5` file holding event traces under the `current_data` group, keyed by event name.

Figures use Arial, Gill Sans or Apple SD Gothic Neo fonts, set via `matplotlib.rc`. If these are not installed, matplotlib falls back to a default font.

## Contact

Max K. Earle, School of Chemistry, Trinity College Dublin. Corresponding authors: Ulrich F. Keyser (ufk20@cam.ac.uk), Casey M. Platnich (casey.platnich@tcd.ie).
