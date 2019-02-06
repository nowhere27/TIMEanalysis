library(readr)
library(caret)

# Variavles
super <- 'G:/SNUBH/data/'
cellDir <- paste(super, 'SP_forFilter/',sep='')
resDir <- paste(super, 'SP_filtered_data/',sep='')

# Load the model
start <- Sys.time()
model <- readRDS("G:/Superpixel_classifier/twoClasses/classifier.rds")

# Do the classification
metric <- data.frame(filename=character(),
                     total=integer(), tumor=integer(),
                     stroma=integer(),LA=integer())
names(metric) <- c('case_name','total', 'tumor','stroma')
fList <- list.files(cellDir,full.names=FALSE,recursive=FALSE)
N <- length(fList)

for(i in 1:N) {
  fName <- substr(fList[i],1,nchar(fList[i])-4)
  print(fName)
  total <- read_csv(paste(cellDir,fName,'.csv',sep=''),col_types=cols(ROI_Brightness_Max="d"))
  nuc <- data.frame(total[,2:232])

  if(nrow(nuc)!=0) {
    prediction <- predict(model,nuc)

    write.csv(data.frame(total[,1],prediction), file=paste(resDir,fName,'.csv',sep=''))
  }

  res <- data.frame(fName,nrow(nuc),length(which(prediction=='Tumor')),length(which(prediction=='Stroma')))
  names(res) <-  c('case_name','total', 'tumor','stroma')
  metric <- rbind(metric,res)
}

write.csv(metric,file=paste(super,'metric_SP.csv',sep=''))
end <- Sys.time()
print(end-start)
