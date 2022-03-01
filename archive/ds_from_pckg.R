rm(list=ls())

# Libraries for optparse
library(stringr,logical.return=F,warn.conflicts=F,quietly=T,verbose=F)
library(optparse,logical.return=F,warn.conflicts=F,quietly=T,verbose=F)

# Optional linux argument
option_list <- list(
  make_option('--dir_dataset',type='character',default=getwd(),help='Path to dataset directory to load files [default WD]'),
  make_option('--dir_output',type='character',default=getwd(),help='Path to output directory [default WD]')
);

# Parse and assign
opt <- parse_args(OptionParser(option_list=option_list))
dir.dataset <- opt$dir_dataset
dir.output <- opt$dir_output

# packageurl <- "http://cran.r-project.org/src/contrib/Archive/ggplot2/ggplot2_0.9.1.tar.gz"
# install.packages(packageurl, repos=NULL, type="source")

# Remaining packages
pckgs <- c('data.table','survival', 'MASS', 'data.table', 'forcats','stringr',
           'coxphf','timereg','dynsurv','eha','RobustAFT',
           'AdapEnetClass','bujar','survJamda.data','CoxRidge','penalized',
           'iC10','rpart', 'TH.data', 'randomForestSRC',
           'coin','frailtySurv','spBayesSurv','tdROC','condSURV',
           'joint.Cox','joineR','JM','NestedCohort','RCASPAR',
           'pec','Ecdat','popEpi','relsurv', 
           'IPWsurvival','hdnom','asaur','AF','Ecdat','smcure','joineR')
for (pp in pckgs) {
  ptest <- tryCatch(library(pp,character.only = T),error=function(e) NA)
  if (is.na(ptest)) {
    install.packages(pp)
  } else {
    library(pp,character.only = T)
  }
}






############################################################
####### ------- COMBINE ALL DATASETS ----------- ###########

# Put in list and store
lst.surv <- 
  list(
    ### --- CRAN PACKAGES --- ###
    # survival
    bladder=list(So=So.bladder, X=X.bladder, id=id.bladder, cr=cr.bladder),
    cancer = list(So=So.cancer, X=X.cancer, id=id.cancer, cr=cr.cancer),
    cgd = list(So = So.cgd, X=X.cgd, id=id.cgd, cr=cr.cgd),
    colon = list(So=So.colon, X=X.colon, id=id.colon, cr=cr.colon),
    flchain = list(So = So.flchain, X=X.flchain, id=id.flchain, cr=cr.flchain),
    heart = list(So = So.heart, X=X.heart, id=id.heart, cr=cr.heart), 
    lung = list(So = So.lung, X=X.lung, id=id.lung, cr=cr.lung), 
    mgus = list(So = So.mgus2, X=X.mgus2, id=id.mgus2, cr=cr.mgus2),
    ovarian = list(So=So.ovarian, X=X.ovarian, id=id.ovarian, cr=cr.ovarian),
    pbc = list(So = So.pbc, X=X.pbc, id=id.pbc, cr=cr.pbc), 
    retinopathy = list(So = So.retinopathy, X=X.retinopathy, id=id.retinopathy, cr=cr.retinopathy),
    veteran = list(So = So.veteran, X=X.veteran, id=id.veteran, cr=cr.veteran),
    nwtco = list(So = So.nwtco, X = X.nwtco, id=id.nwtco, cr=cr.nwtco),
    # MASS 
    aids = list(So = So.aids, X=X.aids, id=id.aids, cr=cr.aids),
    melanoma = list(So = So.melanoma, X=X.melanoma, id=id.melanoma, cr=cr.melanoma),
    # coxphf
    breast = list(So = So.breast, X = X.breast, id=id.breast, cr=cr.breast),
    # timereg
    trace = list(So = So.trace, X = X.trace, id=id.trace, cr=cr.trace),
    csl = list(So = So.csl, X = X.csl, id=id.csl, cr=cr.csl),
    bmt = list(So = So.bmt, X = X.bmt, id=id.bmt, cr=cr.bmt),
    diabetes = list(So = So.diabetes, X = X.diabetes, id=id.diabetes, cr=cr.diabetes),
    # eha
    scania = list(So = So.scania, X = X.scania, id=id.scania, cr=cr.scania),
    oldmort = list(So = So.oldmort, X = X.oldmort, id=id.oldmort, cr=cr.oldmort),
    # RobustAFT
    Z243 = list(So = So.Z243, X = X.Z243, id=id.Z243, cr=cr.Z243),
    # AdapEnetClass
    MCL = list(So = So.MCL, X = X.MCL, id=id.MCL, cr=cr.MCL),
    # bujar
    chop = list(So = So.chop, X = X.chop, id=id.chop, cr=cr.chop),
    # survJamda.data
    breast_norway = list(So = So.breast_norway, X = X.breast_norway, id=id.breast_norway, cr=cr.breast_norway),
    breast_duke = list(So = So.breast_duke, X = X.breast_duke, id=id.breast_duke, cr=cr.breast_duke),
    breast_nc = list(So = So.breast_nc, X = X.breast_nc, id=id.breast_nc, cr=cr.breast_nc),
    # CoxRidge 
    ova = list(So = So.ova, X = X.ova, id=id.ova, cr=cr.ova),
    # penalized
    nki70 = list(So = So.nki70, X = X.nki70, id=id.nki70, cr=cr.nki70),
    # rpart
    stagec = list(So = So.stagec, X = X.stagec, id=id.stagec, cr=cr.stagec),
    # TH.data
    wpbc = list(So = So.wpbc, X = X.wpbc, id=id.wpbc, cr=cr.wpbc),
    # randomForestSRC
    follic = list(So = So.follic, X = X.follic, id=id.follic, cr=cr.follic),
    # coin
    glioma = list(So = So.glioma, X = X.glioma, id=id.glioma, cr=cr.glioma), 
    # frailtySurv
    hdfail = list(So = So.hdfail, X = X.hdfail, id=id.hdfail, cr=cr.hdfail), 
    # spBayesSurv
    leukemia = list(So = So.leukemia, X = X.leukemia, id=id.leukemia, cr=cr.leukemia), 
    # NestedCohort
    zinc = list(So = So.zinc, X = X.zinc, id=id.zinc, cr=cr.zinc), 
    # joint.Cox
    ovarian2 = list(So = So.ovarian2, X = X.ovarian2, id=id.ovarian2, cr=cr.ovarian2), 
    # RCASPAR
    bergamaschi = list(So = So.bergamaschi, X = X.bergamaschi, id=id.bergamaschi, cr=cr.bergamaschi), 
    # IPWsurvival
    divat = list(So = So.divat, X = X.divat, id=id.divat, cr=cr.divat),
    # hdnom
    smart = list(So = So.smart, X = X.smart, id=id.smart, cr=cr.smart), 
    # relsurv
    rdata = list(So = So.rdata, X = X.rdata, id=id.rdata, cr=cr.rdata), 
    # pec
    pbc3 = list(So = So.pbc3, X = X.pbc3, id=id.pbc3, cr=cr.pbc3), 
    cost = list(So = So.cost, X = X.cost, id=id.cost, cr=cr.cost), 
    # JM
    aidsJM = list(So = So.aidsJM, X = X.aidsJM, id=id.aidsJM, cr=cr.aidsJM),
    pbc2 = list(So = So.pbc2, X = X.pbc2, id=id.pbc2, cr=cr.pbc2),  
    # asaur
    hepato = list(So = So.hepato, X = X.hepato, id=id.hepato, cr=cr.hepato), 
    smoking = list(So = So.smoking, X = X.smoking, id=id.smoking, cr=cr.smoking), 
    prostate = list(So = So.prostate, X = X.prostate, id=id.prostate, cr=cr.prostate), 
    # RcmdrPlugin.survival
    dialysis = list(So = So.dialysis, X = X.dialysis, id=id.dialysis, cr=cr.dialysis), 
    rossi = list(So = So.rossi, X = X.rossi, id=id.rossi, cr=cr.rossi), 
    # AF
    rotterdam = list(So = So.rotterdam, X = X.rotterdam, id=id.rotterdam, cr=cr.rotterdam), 
    # Ecdat
    unemp1 = list(So = So.unemp1, X = X.unemp1, id=id.unemp1, cr=cr.unemp1),
    unemp2 = list(So = So.unemp2, X = X.unemp2, id=id.unemp2, cr=cr.unemp2),
    # smcure
    ecog = list(So = So.ecog, X = X.ecog, id=id.ecog, cr=cr.ecog), 
    # joineR
    heartvalve = list(So = So.heartvalve, X = X.heartvalve, id=id.heartvalve, cr=cr.heartvalve), 
    epileptic = list(So = So.epileptic, X = X.epileptic, id=id.epileptic, cr=cr.epileptic), 
    # # pckg
    # VV = list(So = So.VV, X = X.VV),  
    ### --- Lifelines datasets --- ###
    anderson = list(So = So.anderson, X=X.anderson, id=id.anderson, cr=cr.anderson),
    divorce = list(So = So.divorce, X=X.divorce, id=id.divorce, cr=cr.divorce),
    kidney = list(So = So.kidney, X=X.kidney, id=id.kidney, cr=cr.kidney),
    larynx  = list(So = So.larynx, X=X.larynx, id=id.larynx, cr=cr.larynx),
    ### --- Vanderbilt datasets --- ###
    support2 = list(So=So.support2, X=X.support2, id=id.support2, cr=cr.support2),
    gbr = list(So = So.gbr, X = X.gbr, id=id.gbr, cr=cr.gbr),
    byar = list(So = So.byar, X = X.byar, id=id.byar, cr=cr.byar),
    framingham = list(So = So.framingham, X = X.framingham, id=id.framingham, cr=cr.framingham),
    RHC = list(So = So.RHC, X = X.RHC, id=id.RHC, cr=cr.RHC),
    catheter = list(So = So.catheter, X = X.catheter, id=id.catheter, cr=cr.catheter),
    ARI = list(So = So.ARI, X = X.ARI, id=id.ARI, cr=cr.ARI),
    vlbw = list(So = So.vlbw, X = X.vlbw, id=id.vlbw, cr=cr.vlbw),
    ### --- Chandan Reddy
    worcester = list(So = So.worcester, X = X.worcester, id=id.worcester, cr=cr.worcester),
    vdv = list(So = So.vdv, X = X.vdv, id=id.vdv, cr=cr.vdv),
    AML = list(So = So.AML, X = X.AML, id=id.AML, cr=cr.AML),
    DBCD = list(So = So.DBCD, X = X.DBCD, id=id.DBCD, cr=cr.DBCD),
    DLBCL = list(So = So.DLBCL, X = X.DLBCL, id=id.DLBCL, cr=cr.DLBCL),
    NSBCD = list(So = So.NSBCD, X = X.NSBCD, id=id.NSBCD, cr=cr.NSBCD),
    employee = list(So = So.employee, X = X.employee, id=id.employee, cr=cr.employee),
    ### --- churn
    telco = list(So = So.telco, X = X.telco, id=id.telco, cr=cr.telco),
    ### --- OPENML
    lungcaner = list(So = So.lungcancer, X = X.lungcancer, id=id.lungcancer, cr=cr.lungcancer),
    pharynx = list(So = So.pharynx, X = X.pharynx, id=id.pharynx, cr=cr.pharynx),
    ### --- Other
    aids320 = list(So = So.aids320, X = X.aids320, id=id.aids320, cr=cr.aids320),
    microcensure = list(So = So.microcensure, X = X.microcensure, id=id.microcensure, cr=cr.microcensure)
  )

# Make sure that none of our time points end on 0...
for (ss in names(lst.surv)) {
  tmp.So <- lst.surv[[ss]]$So
  if( ncol(tmp.So) == 2 ) {
    tmin <- min(tmp.So[,1])
    if (tmin==0) {
      print(sprintf('Dataset %s has event time at 0, adding 1 to all events times',ss))
      tmp.So[,1] <- tmp.So[,1] + 1
      lst.surv[[ss]]$So <- tmp.So
    }
  }
}

# Get dataset features
ds.timedep <- ifelse(unlist(lapply(lst.surv,function(ll) ncol(ll$So) ))==2,F,T)
ds.cens <- mapply(function(ll, td) 1-ifelse(td, mean(ll$So[,3]), mean(ll$So[,2])),lst.surv,ds.timedep)
ds.n <- unlist(lapply(lst.surv,function(ll) nrow(ll$So) ))
ds.n2 <- unlist(lapply(lst.surv,function(ll) nrow(ll$X) ))
ds.n3 <- unlist(lapply(lst.surv,function(ll) length(ll$id) ))
ds.n4 <- lapply(lst.surv,function(ll) nrow(ll$cr) )
ds.n4 <- unlist(lapply(ds.n4, function(ll) ifelse(is.null(ll),0,ll)))
which(ds.n != ds.n3)
which(ds.n[ds.n4!=0] != ds.n4[ds.n4!=0])
ds.p <- unlist(lapply(lst.surv,function(ll) ncol(ll$X) ))
data.table(dataset=names(ds.n),n=ds.n,n2=ds.n2)[n != n2]

# Organize by n
ds.summary <- data.table(dataset=names(lst.surv), n=ds.n, p=ds.p, events=ds.n*(1-ds.cens), cens=round(ds.cens,2), 
                         timedep=ifelse(ds.timedep,'yes','no'), highdim=ifelse(ds.p > ds.n,'yes','no'))[order(-n)]
# Save the list
format(object.size(lst.surv),'MB')
save(lst.surv, file=file.path(dir.output,'surv_datasets.RData'))

# Make a plot
ds.plot <- melt(ds.summary,measure.vars=c('n','p'),variable.name='dimension')
ds.plot[, dimension := fct_recode(dimension, '# of samples'='n','# of features'='p')]

gg.base <- ggplot() + background_grid(major='xy',minor='none') + 
  facet_wrap(~dimension,scales='free') + 
  theme(axis.title = element_blank(), axis.text.x = element_text(angle=90,size=8),
        legend.position = 'bottom',legend.justification = 'center') + 
  scale_color_gradient(low='blue',high='orange', name='Censoring (%): ')
gg1 <- gg.base + geom_point(data=ds.plot[as.numeric(dimension)==1],aes(x=fct_reorder(dataset,value),y=log2(value), color=cens)) + 
  scale_y_continuous(breaks=seq(0,14,2)) 
tmp.leg <- get_legend(gg1)
gg1 <- gg1 + theme(legend.position = 'none')
gg2 <- gg.base + geom_point(data=ds.plot[as.numeric(dimension)==2],aes(x=fct_reorder(dataset,value),y=log2(value), color=cens)) + 
  scale_y_continuous(breaks=seq(0,18,2)) + guides(color=F)
gg.ds.summary <- plot_grid(plot_grid(gg1, gg2, nrow=1, labels = c('n','p')),tmp.leg,rel_heights = c(10,1),ncol=1)
save_plot(filename = file.path(dir.output,'..','figures','gg_surv_desc.png'),plot=gg.ds.summary, base_height=10,base_width = 14)

