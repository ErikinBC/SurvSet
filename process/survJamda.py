# --- (xxvi) breast_norway [gse4335] --- #
utils::data(gse4335, package = 'survJamda.data')
utils::data(gse4335pheno, package = 'survJamda.data')
# Clinical data
cn.old <- c('Age_at_diagnosis','X._ER_status_.0.neg._1.pos..','T_.tumor_size.',
            'N_.node_status.','M_.metastasis.','Grade','Histology')
cn.new <- c('age','er_status','tumor_size','node_status','metastasis','grade','histology')
X.tmp <- gse4335pheno[,cn.old]
colnames(X.tmp) <- cn.new
# Remove any missing values
idx.keep <- with(X.tmp, which(!(er_status=='na' | tumor_size =='na' | node_status %in% c('na','x') | grade == 'na')))
X.tmp <- X.tmp[idx.keep,]
X.breast_norway.clin <- model.matrix(~age+er_status+tumor_size+node_status+metastasis+grade,data=X.tmp)[,-1]
So.breast_norway <-  with(gse4335pheno[idx.keep,], Surv(time=Overall_survival_.months., event=X.Status_0.A._1.AWD._2.DOD._3.DOC.) )
X.breast_norway <- as.matrix(cbind(X.breast_norway.clin, gse4335[idx.keep,]))
id.breast_norway <- seq(nrow(X.breast_norway))
cr.breast_norway <- NULL

# --- (xxvii) breast_duke [gse4335] --- #
utils::data(gse3143, package = 'survJamda.data')
utils::data(gse3143pheno, package = 'survJamda.data')

So.breast_duke <- with(gse3143pheno, Surv(time=`Survival_Time(months)`,event=`Status(0=alive,1=dead)`))
X.breast_duke <- as.matrix(gse3143)
id.breast_duke <- seq(nrow(X.breast_duke))
cr.breast_duke <- NULL

# --- (xxviii) breast_nc  [gse1992] --- #

utils::data(gse1992)
utils::data(gse1992pheno)

cn.old <- c('Age','ER__.1.positive._0.negative.','Node_status_.1.positive.1_or_more_nodes.._0.negative.',
            'Grade','Size_.1._..2cm._2._.2cm_to_..5cm._3..5cm._4.any_size_with_direct_extension_to_chest_wall_or_skin.',
            'RFS_event_.0.no_relapse.1.relapsed_at_any_site_or_died_of_disease.','RFS_months',
            'Overall_Survival_Event_.0.alive.1.DOD_or_DOC.','Overall_suvival_months')
cn.new <- c('age','er_positive','node_status','grade','size','rfs_event','rfs_months','surv_event','suv_months')
X.tmp <- gse1992pheno[,cn.old]
colnames(X.tmp) <- cn.new
idx.keep <- which(with(X.tmp,!(is.na(er_positive) | is.na(node_status) | is.na(size) | is.na(grade))))
X.tmp <- X.tmp[idx.keep,]
So.breast_nc <- with(X.tmp, Surv(time=rfs_months, event=rfs_event))
X.breast_nc.clin <- model.matrix(~age+factor(er_positive)+factor(node_status)+factor(grade)+factor(size),data=X.tmp)[,-1]
X.breast_nc <- as.matrix(cbind(X.breast_nc.clin, gse1992[idx.keep,]))
id.breast_nc <- seq(nrow(X.breast_nc))
cr.breast_nc <- NULL
