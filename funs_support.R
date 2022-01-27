# Utility functions to help in R

makeifnot = function(path) {
    if (!dir.exists(path)) {
        print('Folder does not exist, creating')
        dir.create(path)
    }
}

