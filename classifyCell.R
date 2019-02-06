library(readr)
library(caret)

# Variavles
super <- 'G:/SNUBH/data/'
cellDir <- paste(super, 'Cell_forFilter/',sep='')
resDir <- paste(super, 'Cell_filtered_data/',sep='')

# Load the model
start <- Sys.time()
CD3_model <- readRDS("G:/Cell_classifier/classifier_CD3.rds")
CD8_model <- readRDS("G:/Cell_classifier/classifier_CD8.rds")

# Do the classification
metric <- data.frame(filename=character(),
                     lympho_total=integer(),
                     lympho_positive=integer())
names(metric) <- c('tile_name','lympho_total','lympho_positive')
fList <- list.files(cellDir,full.names=FALSE,recursive=FALSE)
N <- length(fList)

for(i in 1:N) {
  fName <- substr(fList[i],1,nchar(fList[i])-4)
  print(fName)
  total <- read_csv(paste(cellDir,fName,'.csv',sep=''),col_types=cols(ROI_Brightness_Max="d"))
  nuc <- data.frame(total[,2:126])

  if(nrow(nuc)!=0) {
    if(grepl('CD3',fName))
      prediction <- predict(CD3_model,nuc)
    else
      prediction <- predict(CD8_model,nuc)

    write.csv(data.frame(total[,1],prediction), file=paste(resDir,fName,'.csv',sep=''))
  }

  res <- data.frame(fName,nrow(nuc),length(which(prediction=='Positive')))
  names(res) <-  c('tile_name','lympho_total','lympho_positive')
  metric <- rbind(metric,res)
}

write.csv(metric,file=paste(super,'metric.csv',sep=''))
end <- Sys.time()
print(end-start)
