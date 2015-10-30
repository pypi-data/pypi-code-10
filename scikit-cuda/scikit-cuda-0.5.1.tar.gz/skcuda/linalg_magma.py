import numpy as np

try:
    from . import magma
    _has_magma = True
except (ImportError, OSError):
    _has_magma = False

def magma_svd(a_cpu, jobu='A', jobvt='A'):
    """
    Singular Value Decomposition.

    Factors the matrix `a` into two unitary matrices, `u` and `vh`,
    and a 1-dimensional array of real, non-negative singular values,
    `s`, such that `a == dot(u.T, dot(diag(s), vh.T))`.

    Notes
    -----
    Computes SVD using MAGMA's SVD routine.
    """

    if not _has_magma:
        raise NotImplementError('Magma not installed')
    
    data_type = a_cpu.dtype.type
    real_type = np.float32
    is_complex = False
    
    jobvt, jobu = jobu, jobvt
    N, M = a_cpu.shape
        
    if data_type == np.complex64:
        magma_func = magma.magma_cgesvd
        nb = magma.magma_get_cgesvd_nb(N);
        is_complex=True
        
    elif data_type == np.float32:
        magma_func = magma.magma_sgesvd
        nb = magma.magma_get_sgesvd_nb(N);
        is_float=True
    elif data_type == np.complex128:
        magma_func = magma.magma_zgesvd
        nb = magma.magma_get_zgesvd_nb(N);
        is_complex=True
        
    else:
        magma_func = magma.magma_dgesvd
        nb = magma.magma_get_dgesvd_nb(N);

    
        
    
    # Set the leading dimension of the input matrix:
    lda = max(1, M)
    ldu=M

    jobu=magma.magma_vec_const(jobu)
    jobvt=magma.magma_vec_const(jobvt)
    
    min_nm=np.min([M,N])
    max_nm=np.max([M,N])
    #if is_complex:
    #    lwork_sz = min_nm*min_nm + 2*min_nm + np.max( [2*min_nm*nb, max_nm*nb] )
    #    
    #    #lwork_sz = (M+N)*nb + 2*np.min([M,N]) + 2*np.min([M,N])**2
    #    
    #    #rwork_sz=np.max( [5*min_nm*min_nm + 5*min_nm, 2*max_nm*min_nm + 2*min_nm*min_nm + min_nm,7*min_nm] )
    #    rwork_sz=5*np.min([M,N])
    #    rwork=np.zeros(rwork_sz,np.float64)
    #else:
    #    lwork_sz = min_nm*min_nm + np.max([ 3*min_nm + np.max( [(2*min_nm)*nb, 3*min_nm*min_nm + 4*min_nm]), min_nm + max_nm*nb])
    #    #lwork_sz = (M+N)*nb + 3*np.min([M,N]) + 2*np.min([M,N])**2
        
    if is_complex:
        lwork_sz = (M+N)*nb + 2*np.min([M,N]) + (2*np.min([M,N]))**2
        rwork_sz=5*np.min([M,N])
        rwork=np.zeros(rwork_sz,np.float64)
    else:
        lwork_sz = (M+N)*nb + 3*np.min([M,N]) + 2*np.min([M,N])**2

    ldvt = N
    #allocate the arrays
    u_cpu=np.zeros((ldu,ldu),data_type)
    s_cpu=np.zeros(np.min((M,N)),np.float64)
    vt_cpu=np.zeros((ldvt,ldvt),data_type)
    lwork=np.zeros(lwork_sz,data_type)

    info = np.zeros(1,int)
        
    # Compute SVD and check error status:
    if is_complex:
        status = magma_func(jobu, jobvt, M, N, int(a_cpu.ctypes.data),
                            lda, int(s_cpu.ctypes.data), int(u_cpu.ctypes.data),
                            ldu, int(vt_cpu.ctypes.data), ldvt,lwork.ctypes.data,
                            lwork_sz,rwork.ctypes.data,info.ctypes.data)
    else:
        status = magma_func(jobu, jobvt, M, N, int(a_cpu.ctypes.data),
                            lda, int(s_cpu.ctypes.data), int(u_cpu.ctypes.data),
                            ldu, int(vt_cpu.ctypes.data), ldvt,lwork.ctypes.data,
                            lwork_sz,info.ctypes.data)
        
    return vt_cpu, s_cpu, u_cpu
    
def magma_sdd(a_cpu, jobz='A'):
    """
    Singular Value Decomposition.

    Factors the matrix `a` into two unitary matrices, `u` and `vh`,
    and a 1-dimensional array of real, non-negative singular values,
    `s`, such that `a == dot(u.T, dot(diag(s), vh.T))`. 

    Notes
    -----
    Computes SVD using MAGMA's divide-and-conquer algorithm.
    """

    if not _has_magma:
        raise NotImplementedError('Magma not installed')
    
    data_type = a_cpu.dtype.type
    real_type = np.float32
    is_complex=False
    
    N,M = a_cpu.shape
    
    if data_type == np.complex64:
        magma_func = magma.magma_cgesdd
        nb = magma.magma_get_cgesvd_nb(N);
        is_complex = True
    elif data_type == np.float32:
        magma_func = magma.magma_sgesdd
        nb = magma.magma_get_sgesvd_nb(N);
        is_float = True
    elif data_type == np.complex128:
        magma_func = magma.magma_zgesdd
        nb = magma.magma_get_zgesvd_nb(N);
        is_complex = True
    else:
        magma_func = magma.magma_dgesdd
        nb = magma.magma_get_dgesvd_nb(N);

    # Set the leading dimension of the input matrix:
    lda = max(1, M)
    ldu = M

    jobz = magma.magma_vec_const(jobz)
    
    min_nm = np.min([M, N])
    max_nm = np.max([M, N])
    if is_complex:
        lwork_sz = min_nm*min_nm + 2*min_nm + np.max( [2*min_nm*nb, max_nm*nb] )
        rwork_sz=np.max( [5*min_nm*min_nm + 5*min_nm, 2*max_nm*min_nm + 2*min_nm*min_nm + min_nm,7*min_nm] )
        rwork=np.zeros(rwork_sz,np.float64)
    else:
        lwork_sz = min_nm*min_nm + np.max([ 3*min_nm + np.max( [(2*min_nm)*nb, 3*min_nm*min_nm + 4*min_nm]), min_nm + max_nm*nb])

    ldvt = N

    # Allocate output and work arrays:
    u_cpu=np.zeros((ldu, ldu),data_type)
    s_cpu=np.zeros(np.min((M, N)),np.float64)
    vt_cpu=np.zeros((ldvt,ldvt),data_type)
    lwork=np.zeros(lwork_sz,data_type)

    iwork = np.zeros(8*np.min([M,N]),int)

    
    info = np.zeros(1,int)

    # Compute SVD and check error status:
    if is_complex:
        status = magma_func(jobz, M, N, int(a_cpu.ctypes.data),
                            lda, int(s_cpu.ctypes.data), int(u_cpu.ctypes.data),
                            ldu, int(vt_cpu.ctypes.data), ldvt, lwork.ctypes.data,
                            lwork_sz, rwork.ctypes.data, iwork.ctypes.data,
                            info.ctypes.data)
    else:
        status = magma_func(jobz, M, N, int(a_cpu.ctypes.data),
                            lda, int(s_cpu.ctypes.data), int(u_cpu.ctypes.data),
                            ldu, int(vt_cpu.ctypes.data), ldvt, lwork.ctypes.data,
                            lwork_sz, iwork.ctypes.data, info.ctypes.data)
        
    return vt_cpu,s_cpu,u_cpu
