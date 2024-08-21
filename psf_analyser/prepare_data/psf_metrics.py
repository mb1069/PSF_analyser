from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from skimage.transform import resize


def mean_squared_error(x, y):
    err = np.mean((x - y)**2)
    return err


def reduce_img(stack):
    return stack.max(axis=(1, 2))


def resize_side_profile(img):
    return resize(img, (img.shape[0], 30))


def get_lat_fwhm(stack, px_size_xy, debug=False):
    def gaussian_2d(xy, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
        x, y = xy
        xo = float(xo)
        yo = float(yo)
        a = (np.cos(theta)**2) / (2 * sigma_x**2) + (np.sin(theta)**2) / (2 * sigma_y**2)
        b = -(np.sin(2 * theta)) / (4 * sigma_x**2) + (np.sin(2 * theta)) / (4 * sigma_y**2)
        c = (np.sin(theta)**2) / (2 * sigma_x**2) + (np.cos(theta)**2) / (2 * sigma_y**2)
        g = offset + amplitude * np.exp(- (a * ((x - xo)**2) + 2 * b * (x - xo) * (y - yo) + c * ((y - yo)**2)))
        return g.ravel()

    sharp = reduce_img(stack)
    idx = np.argmax(sharp)
    image = stack[idx]

    # Load and preprocess the image (e.g., convert to grayscale)
    # For simplicity, let's generate a simple image for demonstration
    image_size = image.shape[1]
    x = np.linspace(0, image_size - 1, image_size)
    y = np.linspace(0, image_size - 1, image_size)
    x, y = np.meshgrid(x, y)

    image = image / image.max()

    # Fit the Gaussian to the image data
    p0 = [1, image_size / 2, image_size / 2, 2, 2, 0, 0]  # Initial guess for parameters
    bounds = [
        (0, np.inf),
        (image_size * (1 / 5), image_size * (4 / 5)),
        (image_size * (1 / 5), image_size * (4 / 5)),
        (0, image_size / 3),
        (0, image_size / 3),
        (-np.inf, np.inf),
        (0, np.inf),
    ]

    try:
        popt, _ = curve_fit(gaussian_2d, (x, y), image.ravel(), p0=p0, bounds=list(zip(*bounds)))
    except RuntimeError:
        popt = p0
    render = gaussian_2d((x, y), *popt).reshape(image.shape)

    error = mean_squared_error(render, image)
    # if error > mse_thres:
    #     fwhm_x, fwhm_y =  np.nan, np.nan
    # else:
    amplitude, xo, yo, sigma_x, sigma_y, theta, offset = popt
    f = 2 * np.sqrt(2 * np.log(2))
    fwhm_x = sigma_x * f * px_size_xy
    fwhm_y = sigma_y * f * px_size_xy
    fwhm_xy = np.mean([fwhm_x, fwhm_y])

    if debug:
        plt.figure(figsize=(2, 2))
        print('FWHM x:', round(fwhm_x, 3), 'nm')
        print('FWHM y:', round(fwhm_y, 3), 'nm')
        print('MSE   :', '{:.2e}'.format(error))
        plt.imshow(image)
        plt.show()
        print('\n')
    return fwhm_xy, error


def norm_min_max(z):
    return (z - z.min()) / (z.max() - z.min())


def get_axial_fwhm(stack, z_step, debug=False, mse_thres=0.001):

    def skewed_gaussian(x, A, x0, sigma, alpha, offset):
        """
        A: Amplitude
        x0: Center
        sigma: Standard Deviation
        alpha: Skewness parameter
        offset: Vertical offset
        """
        return A * np.exp(-(x - x0)**2 / (2 * sigma**2)) * (1 + erf(alpha * (x - x0))) + offset

    z_profile = stack.max(axis=(1, 2))
    z_profile = norm_min_max(z_profile)

    # Fit the Gaussian to the image data
    p0 = [z_profile.max(), np.argmax(z_profile), len(z_profile) / 10, 0, np.mean(z_profile)]  # Initial guess for parameters
    bounds = [
        (0, z_profile.max()),
        (0, len(z_profile)),
        (0, len(z_profile)),
        (-1, 1),
        (0, z_profile.max()),
    ]

    x = np.arange(len(z_profile))
    try:
        popt, pcov = curve_fit(skewed_gaussian, x, z_profile, p0=p0, bounds=list(zip(*bounds)))
    except RuntimeError:
        popt = p0
    render = skewed_gaussian(x, *popt)

    A, x0, sigma, alpha, offset = popt
    error = mean_squared_error(render, z_profile)

    f = 2 * np.sqrt(2 * np.log(2))
    fwhm_z = sigma * f

    fwhm_z *= z_step

    if debug:
        print('FWHM z:', round(fwhm_z, 3))
        print('MSE   :', '{:.2e}'.format(error))
        plt.plot(render, label='fit')
        plt.plot(z_profile, label='data')
        plt.legend()
        plt.show()
    return fwhm_z, error


def get_projections(stack, zstep, zrange=2000):
    peak = np.argmax(stack.max(axis=(1, 2)))
    start = max(int(peak - np.ceil(zrange / zstep)), 0)
    end = int(peak + np.ceil(zrange / zstep))

    s = stack[start:end]

    fig, axs = plt.subplots(3, 1, layout='constrained', figsize=(4, 10))

    # xy view
    img = s.sum(axis=(0))
    axs[0].imshow(img)
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Y')

    # zy
    img = s.sum(axis=1)
    axs[1].imshow(resize_side_profile(img))
    axs[1].set_xlabel('Y')
    axs[1].set_ylabel('Z')

    # zx
    img = s.sum(axis=2)
    axs[2].imshow(resize_side_profile(img))
    axs[2].set_xlabel('X')
    axs[2].set_ylabel('Z')

    return fig
