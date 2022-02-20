# Script to process datasets not found in R packages

# # --- (vii) employee_attrition.csv --- #
# tmp.dat <- fread(file.path(dir.reddy, 'employee_attrition.csv'))
# tmp.dat[, BusinessTravel := factor(BusinessTravel, levels=c('Travel_Rarely','Travel_Frequently','Non-Travel'))]
# So.employee <- with(tmp.dat, Surv(time=YearsAtCompany,Attrition=='Yes') )

# X.employee <- model.matrix(~Age + BusinessTravel + DailyRate + Department + DistanceFromHome + 
#                Education + EducationField + EnvironmentSatisfaction + Gender + HourlyRate + 
#                JobInvolvement + JobLevel + JobRole + JobSatisfaction + MaritalStatus + 
#                MonthlyIncome + MonthlyRate + NumCompaniesWorked + OverTime + PercentSalaryHike + 
#                PerformanceRating + RelationshipSatisfaction + StockOptionLevel + TrainingTimesLastYear, data=tmp.dat)[,-1]
# id.employee <- seq(nrow(X.employee))
# cr.employee <- NULL

# # https://www.openml.org/d/1245
# # --- (i) lungcancer - Shedden [phpl04K8a] --- #
# tmp.dat <- fread(file.path(dir.openml,'phpl04K8a.csv'))
# cn.clean <- c('OS_event','histology','sex')
# tmp.dat[, (cn.clean) := lapply(.SD, function(ll) str_remove_all(ll,"\\'")), .SDcols=cn.clean]
# tmp.dat[, `:=` (OS_years = round(OS_years, 3), OS_event=as.numeric(OS_event))]
# X.lungcancer <- model.matrix(~., data=tmp.dat[,-(1:3)])[,-1]
# So.lungcancer <- with(tmp.dat, Surv(time=OS_years, event=OS_event))
# id.lungcancer <- seq(nrow(X.lungcancer))
# cr.lungcancer <- NULL
