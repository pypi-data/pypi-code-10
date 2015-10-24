# Based on qvalue R package 

def qvalue(pvalues, lambdas=[0,0.90,0.05], pi0_method="smoother",
    fdr_level=None, robust=False,  smoot_df=3, smooth_log_pi0=False):
    """Estimate the q-values for a given set of p-values

    Estimate the q-values for a given set of p-values.  The q-value of
    a test measures the proportion of false positives incurred (called
    the false discovery rate) when that particular test is called
    significant.

    If no options are selected, then the method used to estimate pi_0
    is the smoother method described in Storey and Tibshirani (2003).
    The bootstrap method is described in Storey, Taylor & Siegmund
    (2004).


    :param p: A vector of p-values (only necessary input)

    :param lambdas: The value of the tuning parameter to estimate pi_0. Must be
          in [0,1). 

    :param pi0_method: Either "smoother" or "bootstrap"; the method for
          automatically choosing tuning parameter in the estimation of
          pi_0, the proportion of true null hypotheses

    :param fdr_level: A level at which to control the FDR. Must be in (0,1].
          Optional; if this is selected, a vector of TRUE and FALSE is
          returned that specifies whether each q-value is less than
          fdr_level or not.

    :param robust: An indicator of whether it is desired to make the estimate
          more robust for small p-values and a direct finite sample
          estimate of pFDR. Optional.

    :param smooth_df: Number of degrees-of-freedom to use when estimating pi_0
          with a smoother. Optional.

    :param smooth_log_pi0: If TRUE and 'pi0_method' = "smoother", pi_0 will be
          estimated by applying a smoother to a scatterplot of log pi_0
          Estimate the q-values for a given set of p-values
    """
    if min(pvalues)<0 or max(pvalues)>1:
        raise ValueError("pvalues must be in the range[0, 1]")

    if len(lambdas>1) and len(lambdas)<4:
        raise ValueError("""if length of lambda greater than 1, you need at least 4 values""")

    if len(lambdas) >= 1 and (min(lambdas<0) or max(lambdas)>=1):
        raise ValueError("lambdas must be in the range[0, 1[")

    m = len(pvalues)
    if len(lambdas) == 1:
        pi0 = mean(p>=lambdas)/(1-lambdas)
        pi0 = min(pi0, 1)
    else:
        pi0 - range(0,len(lambdas))
        for i in range(0,len(lambdas)):
            pi0[i] <- mean(p >= lambdas[i])/(1 - lambdas[i])

        if (pi0.method == "smoother"):
            if (smooth.log.pi0):
                pi0 <- log(pi0)
            #spi0 <- smooth.spline(lambdas, pi0, df = smooth.df)
            #pi0 <- predict(spi0, x = max(lambdas))$y
            if (smooth_log_pi0):
                pi0 <- exp(pi0)
            pi0 = min(pi0, 1)

        elif (pi0.method == "bootstrap"):
            minpi0 = min(pi0)
            mse = rep(0, len(lambdas))
            pi0.boot = rep(0, len(lambdas))
            for i in range(1,100):
                p.boot = sample(p, size = m, replace = TRUE)
                for i in range(0,len(lambdas)):
                    pi0.boot[i] <- mean(p.boot > lambdas[i])/(1 - lambdas[i])
                mse = mse + (pi0.boot - minpi0)^2

            pi0 = min(pi0[mse == min(mse)])
            pi0 = min(pi0, 1)
        else:
           raise ValueError("'pi0.method' must be one of 'smoother' or 'bootstrap'.")

    if pi0 <= 0:
        raise ValueError("""The estimated pi0 <= 0. Check that you have valid p-values or use another lambda method.""")
        return

    #if (!is.null(fdr_level) && (fdr_level <= 0 || fdr_level > 1)):
    #    raise ValueError("ERROR: 'fdr_level' must be within (0, 1].")

    u = order(p)
    def qvalue_rank(x):
        idx = sort.list(x)
        fc = factor(x)
        nl = len(levels(fc))
        bin = int(fc)
        tbl = tabulate(bin)
        cs = cumsum(tbl)
        tbl = rep(cs, tbl)
        tbl[idx] = tbl
        return tbl

    v = qvalue-rank(p)
    qvalue = pi0 * m * p/v
    if robust is True:
        qvalue = pi0 * m * p/(v * (1 - (1 - p)^m))

    qvalue[u[m]] = min(qvalue[u[m]], 1)
    # FIXME indices here below are from R
    for i in range((m - 1),1):
        qvalue[u[i]] = min(qvalue[u[i]], qvalue[u[i + 1]], 1)

    #if (!is.null(fdr_level)):
    #    retval = {'call': match.call(), 'pi0': pi0, 'qvalues': qvalue,
    #        'pvalues': pvalues, 'fdr_level': fdr_level, 
    #        'significant': (qvalue <=  fdr_level), 
    #        'lambdas': lambdas}

    #else:
    #    retval = {'call': match.call(), 'pi0': pi0, 'qvalues': qvalue,
    #        'pvalues': pvalues, 'lambdas': lambdas)
    retval = {}
    return retval













