
Among the various adult brain tumors, glioblastoma (GBM) is arguably the most aggressive, infiltrative, and heterogeneous. Biophysical modeling of GBM growth has
shown its importance, towards contributing to more informed clinical decision-making. However, developing a mathematical framework that accurately captures 
biophysical GBM growth in individual patients poses numerous challenges, ranging from prohibitive computational costs, ill-posedness of the inverse problem, to 
model design and selection.
We present a deep learning (DL)-based logistical regression model to estimate the GBM's biophysical growth in seconds. This growth is defined by three 
tumor-specific parameters: 1) a diffusion coefficient in white matter (Dw), which prescribes the rate of infiltration of tumor cells in white matter, 2) a
mass-effect parameter (Mp), which defines the average tumor expansion, and 3) the estimated time (T) in number of days that the tumor has been growing.
Preoperative structural multi-parametric MRI (mpMRI) scans from $n=135$ subjects of the TCGA-GBM imaging collection are used to quantitatively evaluate our 
approach. We consider the mpMRI intensities within the region defined by the abnormal FLAIR signal envelope for training one DL model for each of the 
tumor-specific growth parameters. We train and validate the DL-based predictions against parameters derived from biophysical inversion models. The average Pearson 
correlation coefficients between our DL-based estimations and the biophysical parameters are $0.85$ for $Dw$, $0.90$ for $Mp$, and $0.94$ for $T$, respectively. 
This study unlocks the power of tumor-specific parameters from biophysical tumor growth estimation. It paves the way towards their clinical translation and opens 
the door for leveraging advanced radiomic descriptors in future studies by means of a significantly faster parameter reconstruction compared to biophysical growth 
modeling approaches.
