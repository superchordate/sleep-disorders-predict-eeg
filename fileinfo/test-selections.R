# test selections of signals to what files will be available for given input sets.

require(easyr)
begin()

t = read.any('../edfinfo.csv')

reqs = c(
  `C4-A1` = 128,
  `C4-P4` = 128,
  `DX1-DX2` = 128,
  `ECG1-ECG2` = 128,
  `EMG1-EMG2` = 128,
  `F4-C4` = 128,
  `Fp2-F4` = 128,
  #`F8-T4` = 128,
  #`F7-T3` = 128,
  `Fp2-F4` = 128,
  `P4-O2` = 128,
  #PLETH = 128,
  `ROC-LOC` = 128,
  SAO2 = 1,
  `SX1-SX2` = 1
)

okfiles = unique(t$file)
for(i in names(reqs)){
  okfiles %<>% intersect(unique(
    t$file[ t$label == i & t$sample_rate >= reqs[[i]] ]
  ))
  cat(i, length(okfiles), '\t')
}

length(okfiles)
table(gsub('[0-9]', '', okfiles))

w(data.frame(label = names(reqs), sample_rate = reqs), '../out/selected-signals')
w(data.frame(file = okfiles), '../out/selected-files')
