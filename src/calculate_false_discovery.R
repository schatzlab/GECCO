library(qvalue)
p <- scan("pvalues.txt")
qobj <- qvalue(p)
qwrite(qobj, filename="qvalue_report.txt")
