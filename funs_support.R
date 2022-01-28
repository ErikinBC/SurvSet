# --- Utility functions to help in R --- #

# Make a folder if it does not exist
makeifnot = function(path) {
    if (!dir.exists(path)) {
        print('Folder does not exist, creating')
        dir.create(path)
    }
}

# Extract filename from the url
get_fn_url = function(url) {
    lst = strsplit(url,'/')[[1]]
    fn = tail(lst,1)
    if (!grepl('.csv$', fn)) {
        fn = paste0(fn, '.csv')
    }
    return (fn)
}


# Function to count categorical features
bin_count <- function(df) {
  df <- as.data.frame(df)
  idx.u <- apply(df,2,function(cc) length(unique(cc)))
  idx.leq <- which(idx.u <= 12)
  if (length(idx.leq) > 0) {
    print(apply(df[,idx.leq,drop=F],2,table))
    propv <- apply(df[,which(idx.u <= 12),drop=F],2,function(cc) min(prop.table(table(cc))) )
    if ( any(propv < 0.05) ) {
      print('The following features have a class imbalance < 5%')
      print(propv[propv < 0.05])
    }  
  }
}
