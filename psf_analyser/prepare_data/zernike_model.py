import numpy as np
from pyotf.phaseretrieval import retrieve_phase
from pyotf.utils import prep_data_for_PR, center_data

def mse(y, y_pred):
    return np.mean((y - y_pred) ** 2).sum()

def norm_zero_one(x):
    return (x-x.min()) / (x.max()-x.min())
    

def get_rms_zerns(pcoefs):
    # Exclude piston tip, tilt and defocus
    return np.sqrt(np.mean(pcoefs[3:]))

def model_psf_zerns(target_psf, model_kwargs, n_zerns=16):
    target_psf = center_data(target_psf)
    # Units of pupil display
    target_psf_prep = prep_data_for_PR(target_psf, multiplier=1.1)
    # Retrieve phase for experimental PSF
    PR_result = retrieve_phase(target_psf_prep, model_kwargs, max_iters=1000, mse_tol=1e-5, pupil_tol=1e-5)
    
    PR_result.fit_to_zernikes(n_zerns)

    result_psf = PR_result.generate_zd_psf(sphase=slice(None))

    target_psf_prep = norm_zero_one(target_psf_prep.astype(float))
    result_psf = norm_zero_one(result_psf.astype(float))
    
    # if disp:
    #     PR_result.plot()
    #     PR_result.zd_result.plot()
    #     PR_result.plot_convergence()
    #     PR_result.model.PSFi = target_psf_prep
    #     PR_result.model.plot_psf()
        
    #     PR_result.model.PSFi = result_psf
    #     PR_result.model.plot_psf()
        
    #     plt.show()
    #     show_psf_axial(target_psf_prep, 'Target', 15)
    #     show_psf_axial(result_psf, 'Result', 15)
    #     show_psf_axial(np.abs(result_psf-target_psf), 'diff', 15)

    #     plt.plot(target_psf_prep.max(axis=(1,2)))
    #     plt.plot(result_psf.max(axis=(1,2)))
    #     plt.show()



    mse = np.mean((target_psf_prep-result_psf)**2)
    zerns =  PR_result.zd_result
    rmse = get_rms_zerns(zerns.pcoefs)
    return zerns.mcoefs, zerns.pcoefs, mse, rmse

# for n_zerns in [8, 16, 32, 64, 128]:
#     print(n_zerns, end=' ')
#     model_psf(target_psf, True, n_zerns)
