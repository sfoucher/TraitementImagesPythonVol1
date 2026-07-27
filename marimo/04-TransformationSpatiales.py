import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams["image.aspect"]= 'equal'
    plt.rcParams['figure.dpi'] = 100
    import warnings
    warnings.filterwarnings('ignore')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Transformations spatiales

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous abordons quelques techniques de traitement d'images dans le domaine spatial uniquement. Ce chapitre est aussi disponible sous la forme d'un notebook Python sur Google Colab:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/04-TransformationSpatiales.ipynb)

    ### Librairies

    Les librairies utilisées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

    -   [scikit-image](https://scikit-image.org/)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` doit être installé:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez les importations:
    """)
    return


@app.cell
def _():
    import numpy as np
    import numpy.fft
    import rioxarray as rxr
    from scipy import signal, ndimage
    import xarray as xr
    import xrscipy
    from skimage import data, measure, graph, segmentation, color
    from skimage.color import rgb2gray
    from skimage.segmentation import slic, mark_boundaries
    import pandas as pd

    return (
        color,
        graph,
        mark_boundaries,
        measure,
        ndimage,
        np,
        numpy,
        pd,
        rgb2gray,
        rxr,
        segmentation,
        signal,
        slic,
        xr,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Images utilisées

    Nous utilisons les images suivantes dans ce chapitre:
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # import gdown
    # 
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a4PQ68Ru8zBphbQ22j0sgJ4D2quw-Wo6', output= 'landsat7.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez que vous êtes capable de les lire :
    """)
    return


@app.cell
def _(rxr):
    with rxr.open_rasterio('berkeley.jpg', mask_and_scale= True) as img_rgb:
        print(img_rgb)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale= True) as img_rgbnir:
        print(img_rgbnir)
    with rxr.open_rasterio('SAR.tif', mask_and_scale= True) as img_SAR:
        print(img_SAR)
    return img_SAR, img_rgb


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Analyse fréquentielle

    L'analyse fréquentielle, issue du traitement du signal, permet d'avoir un autre point de vue sur les données à partir de ses composantes harmoniques. La modification de ces composantes de Fourier modifie l'ensemble de l'image et permet de corriger des problèmes systématiques comme des artefacts ou du bruit de capteur. Bien que ce domaine soit un peu éloigné de la télédétection, les images issues des capteurs sont toutes sujettes à des étapes de traitement du signal et il faut donc en connaître les grands principes afin de pouvoir comprendre certains enjeux lors des traitements.

    ### La transformée de Fourier

    La transformée de Fourier permet de transformer une image dans un espace fréquentielle. Cette transformée est complètement réversible. Dans le cas des images numériques, on parle de `2D-DFT` (*2D-Discrete Fourier Transform*) qui est un algorithme optimisé pour le calcul fréquentiel [@Cooley-1965]. La *1D-DFT* peut s'écrire simplement comme une projection sur une série d'exponentielles complexes:

    $$X[k] = \sum_{n=0 \ldots N-1} x[n] \times \exp(-j \times 2\pi \times k \times n/N))$$ {#eq-dft}

    La transformée inverse prend une forme similaire:

    $$x[k] = \frac{1}{N}\sum_{n=0 \ldots N-1} X[n] \times \exp(j \times 2\pi \times k \times n/N))$$ {#eq-idft}

    Le signal d'origine est donc reconstruit à partir d'une somme de sinusoïdes complexes $\exp(j2\pi \frac{k}{N}n))$ de fréquence $k/N$. Noter qu'à partir de $k=N/2$, les sinusoïdes se répètent à un signe près et forment un miroir des composantes, la convention est alors de mettre ces composantes dans une espace négatif $[-N/2,\ldots,-1]$.

    Dans le cas d'un simple signal périodique à une dimension avec une fréquence de 4/16 (donc 4 périodes sur 16) on obtient deux pics de fréquence à la position de 4 cycles observés sur $N=16$ observations. Les puissances de Fourier sont affichées dans un espace fréquentiel en cycles par unité d'espacement de l'échantillon (avec zéro au début) variant entre -1 et +1. Par exemple, si l'espacement des échantillons est en secondes, l'unité de fréquence est cycles/seconde (ou Hz). Dans le cas de N échantillons, le pic sera observé à la fréquence $+/- 4/16=0.25$ cycles/secondes. La fréquence d'échantillonnage $F_s$ du signal a aussi beaucoup d'importance et doit être au moins à deux fois la plus haute fréquence observée (ici $F_s > 0.5$) sinon un phénomène de repliement appelé aliasing sera observé.
    """)
    return


@app.cell
def _(np, plt, xr):
    import math
    Fs = 2.0
    Ts = 1 / Fs
    N = 16
    _arr = xr.DataArray(np.sin(2 * math.pi * np.arange(0, N, Ts) * 4 / 16), dims='x', coords={'x': np.arange(0, N, Ts)})
    fourier = np.fft.fft(_arr)
    freq = np.fft.fftfreq(fourier.size, d=Ts)
    fourier = xr.DataArray(fourier, dims='f', coords={'f': freq})
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    plt.subplot(1, 2, 1)
    _arr.plot.line(color='red', linestyle='dashed', marker='o', markerfacecolor='blue')
    _axes[0].set_title('Signal périodique')
    plt.subplot(1, 2, 2)
    np.abs(fourier).plot.line(color='red', linestyle='dashed', marker='o', markerfacecolor='blue')
    _axes[1].set_title('Composantes de Fourier (amplitude)')
    plt.show()
    return (math,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtrage fréquentiel

    Un filtrage fréquentiel consiste à modifier le spectre de Fourier afin d'éliminer ou de réduire certaines composantes fréquentielles. On distingue habituellement trois catégories de filtres fréquentiels:

    1.  Les filtres passe-bas qui ne préservent que les basses fréquences pour, par exemple, lisser une image.

    2.  Les filtres passe-hauts qui ne préservent que les hautes fréquences pour ne préserver que les détails.

    3.  Les filtres passe-bandes qui vont préserver les fréquences dans une bande de fréquence particulière.

    La librairie `Scipy` contient différents filtres fréquentiels. Notez, qu'un filtrage fréquentielle est une simple multiplication de la réponse du filtre $F[k]$ par les composantes fréquentielles du signal à filtrer $X[k]$:

    $$
    X_f[k] = F[k] \times X[k]
    $$ {#eq-fourier-filter}

    À noter que cette multiplication dans l'espace de Fourier est équivalente à une opération de convolution dans l'espace originale du signal $x$:

    $$
    x_f = IDFT^{-1}[F]*x
    $$ {#eq-convolve}
    """)
    return


@app.cell
def _(img_rgb, ndimage, numpy, plt):
    (_fig, (ax1, ax2)) = plt.subplots(1, 2, figsize=(10, 4))
    input_ = numpy.fft.fft2(img_rgb.to_numpy())
    result = [ndimage.fourier_gaussian(input_[b], sigma=4) for b in range(3)]  # on filtre chaque bande avec un filtre Gaussien
    result = numpy.fft.ifft2(result)
    ax1.imshow(img_rgb.to_numpy().transpose(1, 2, 0).astype('uint8'))
    ax1.set_title('Originale')
    ax2.imshow(result.real.transpose(1, 2, 0).astype('uint8'))  # La partie imaginaire n'est pas utile ici
    ax2.set_title('Filtrage Gaussien')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### L'aliasing

    L'aliasing est un problème fréquent en traitement du signal. Il résulte d'une fréquence d'échantillonnage trop faible par rapport au contenu fréquentielle du signal. Cela peut se produire lorsque vous sous-échantillonner fortement une image avec un facteur de décimation (par exemple un pixel sur deux). En prenant un pixel sur deux, on réduit la fréquence d'échantillonnage d'un facteur 2 ce qui réduit le contenu fréquentiel de l'image et donc les fréquences maximales de l'image. L'image présente alors un aspect faussement texturée avec beaucoup de hautes fréquences:
    """)
    return


@app.cell
def _(img_rgb, plt):
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    plt.subplot(1, 2, 1)
    img_rgb.astype('int').plot.imshow(rgb='band')
    _axes[0].set_title('Originale')
    plt.subplot(1, 2, 2)
    img_rgb[:, ::4, ::4].astype('int').plot.imshow(rgb='band')
    _axes[1].set_title('Décimée par un facteur 4')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Une façon de réduire le contenu fréquentiel est de filtrer par un filtre passe-bas pour réduire les hautes fréquences par exemple avec un filtre Gaussien:
    """)
    return


@app.cell
def _(img_rgb, math, plt, xr):
    from scipy.ndimage import gaussian_filter
    q = 4
    sigma = q * 1.1774 / math.pi
    _arr = xr.DataArray(gaussian_filter(img_rgb.to_numpy(), sigma=(0, sigma, sigma)), dims=('band', 'y', 'x'), coords={'x': img_rgb.coords['x'], 'y': img_rgb.coords['y'], 'spatial_ref': 0})
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    plt.subplot(1, 2, 1)
    img_rgb.astype('int').plot.imshow(rgb='band')
    _axes[0].set_title('Originale')
    plt.subplot(1, 2, 2)
    _arr[:, ::q, ::q].astype('int').plot.imshow(rgb='band')
    _axes[1].set_title('Décimée par un facteur 4')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La fonction [`decimate`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html#scipy.signal.decimate) dans `scipy.signal` réalise l'opération de décimation (*downsampling*) en une seule étape:
    """)
    return


@app.cell
def _(img_rgb, plt):
    import xrscipy.signal as dsp
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    plt.subplot(1, 2, 1)
    img_rgb.astype('int').plot.imshow(rgb='band')
    _axes[0].set_title('Originale')
    plt.subplot(1, 2, 2)
    dsp.decimate(img_rgb, q=4, dim='x').astype('int').plot.imshow(rgb='band')
    _axes[1].set_title('Décimée par un facteur 4')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Filtrage d'image

    Le filtrage d'image a plusieurs objectifs en télédétection:

    1.  La réduction du bruit afin d'améliorer la résolution radiométrique et améliorer la lisibilité de l'image.

    2.  Le réhaussement de l'image afin d'améliorer le contraste ou faire ressortir les contours.

    3.  La production de nouvelles caractéristiques, c.-à.-d dérivées de nouvelles images mettant en valeur certaines informations dans l'image comme la texture, les contours, etc.

    Il existe de nombreuses méthodes de filtrage dans la littérature qui sont habituellement regroupées en quatre catégories:

    1.  Le filtrage peut-être global ou local, c.-à.-d qu'il prend en compte soit toute l'image pour filtrer (ex: filtrage par Fourier), soit uniquement avec une fenêtre ou un voisinage local.

    2.  La fonction de filtrage peut-être linéaire ou non linéaire.

    3.  La fonction de filtrage peut être stationnaire ou adaptative.

    4.  Le filtrage peut-être mono-échelle ou multi-échelle.

    La librairie `Scipy` ([Multidimensional image processing (scipy.ndimage)](https://docs.scipy.org/doc/scipy/reference/ndimage.html)) contient une panoplie complète de filtres.

    ### Filtrage linéaire stationnaire

    Un filtrage linéaire stationnaire consiste à appliquer une même pondération locale des valeurs des pixels dans une fenêtre glissante. La taille de cette fenêtre est généralement un chiffre impair (3,5, etc.) afin de définir une position centrale et une fenêtre symétrique. La valeur calculée à partir de tous les pixels dans la fenêtre est alors attribuée au pixel central.

    Le filtre le plus simple est certainement le filtre moyen qui consiste à appliquer le même poids uniforme dans la fenêtre glissante. Par exemple pour un filtre 5x5:

    $$
    F= \frac{1}{25}\left[
    \begin{array}{c|c|c|c|c}
    1 & 1 & 1 & 1 & 1 \\
    \hline
    1 & 1 & 1 & 1 & 1 \\
    \hline
    1 & 1 & 1 & 1 & 1 \\
    \hline
    1 & 1 & 1 & 1 & 1 \\
    \hline
    1 & 1 & 1 & 1 & 1
    \end{array}
    \right]
    $$ {#eq-boxfilter}

    En python, on dispose des fonctions `rolling` et `sliding_window` définis dans la librairie `numpy`. Par exemple pour le cas du filtre moyen, on construit une nouvelle vue de l'image avec deux nouvelles dimensions `x_win` et `y_win`:
    """)
    return


@app.cell
def _(img_rgb):
    rolling_win = img_rgb.rolling(x=5, y=5,  min_periods= 3, center= True).construct(x="x_win", y="y_win", keep_attrs= True)
    print(rolling_win[0,0,1,...])
    print(rolling_win.shape)
    return (rolling_win,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'avantage de cette approche est qu'il n'y a pas d'utilisation inutile de la mémoire. Noter les `nan` sur les bords de l'image car la fenêtre déborde sur les bordures de l'image. Par la suite un opérateur de moyenne peut être appliqué sur les axes `x_win` et `y_win` correspondant aux fenêtres glissantes.
    """)
    return


@app.cell
def _(plt, rolling_win):
    filtre_moyen = rolling_win.mean(dim=['x_win', 'y_win'], skipna=True)
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
    filtre_moyen.astype('int').plot.imshow(rgb='band')
    _ax.set_title('Filtre moyen 5x5')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lorsque la taille $W$ de la fenêtre devient trop grande, il est préférable d'utiliser une convolution dans le domaine fréquentielle. La fonction `fftconvolve` de la librairie `scipy.signal` offre cette possibilité:
    """)
    return


@app.cell
def _(img_rgb, np, signal):
    _kernel = np.outer(signal.windows.gaussian(70, 8), signal.windows.gaussian(70, 8))
    _kernel = np.tile(_kernel, (3, 1, 1))
    # notez la répétition du kernel 3x pour traiter une image rgb :
    blurred = signal.fftconvolve(img_rgb, _kernel, mode='same')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Filtrage par convolution

    La façon la plus efficace d'appliquer un filtre linéaire est d'appliquer une convolution. La convolution est généralement très efficace car elle est peut être calculée dans le domaine fréquentiel. Prenons l'exemple du filtre de Scharr [@Scharr1999], qui permet de détecter les contours horizontaux et verticaux:

    $$
    F= \left[
    \begin{array}{ccc}
    -3-3j & 0-10j & +3-3j \\
    -10+0j & 0+0j & +10+0j \\
    -3+3j & 0+10j & +3+3j
    \end{array}
    \right]
    $$ {#eq-scharr-filter}

    Remarquez l'utilisation de chiffres complexes afin de passer deux filtres différents sur la partie réelle et imaginaire.
    """)
    return


@app.cell
def _(img_rgb, np, plt, signal, xr):
    scharr = np.array([[-3 - 3j, 0 - 10j, +3 - 3j], [-10 + 0j, 0 + 0j, +10 + 0j], [-3 + 3j, 0 + 10j, +3 + 3j]])
    print(img_rgb.isel(band=0).shape)
    grad = signal.convolve2d(img_rgb.isel(band=0), scharr, boundary='symm', mode='same')  # Gx + j*Gy
    _arr = xr.DataArray(np.abs(grad), dims=('y', 'x'), coords={'x': img_rgb.coords['x'], 'y': img_rgb.coords['y'], 'spatial_ref': 0})
    print(_arr)
    # on reconstruit un xarray à partir du résultat:
    (_fig, _ax) = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))
    _arr.plot.imshow()
    _ax.set_title('Amplitude du filtre de Scharr')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtrage non linéaire : médian et morphologie mathématique

    Contrairement au filtre moyen ou à la convolution par Scharr, un filtre non linéaire ne peut pas s'exprimer comme une simple pondération des pixels voisins. Le **filtre médian** en est l'exemple le plus courant : il remplace chaque pixel par la médiane des valeurs dans la fenêtre, ce qui élimine efficacement le bruit impulsionnel (*sel et poivre*) tout en préservant mieux les contours qu'un filtre moyen de même taille [@Jensen2016] :
    """)
    return


@app.cell
def _(img_rgb, np, plt):
    from scipy.ndimage import median_filter, uniform_filter
    bruite = img_rgb.to_numpy().astype(float).copy()
    # on ajoute du bruit impulsionnel pour illustrer la différence
    mask = np.random.random(bruite.shape) < 0.05
    bruite[mask] = np.random.choice([0, 255], size=mask.sum())
    filtre_moyen_np = uniform_filter(bruite, size=(1, 5, 5))
    filtre_median_np = median_filter(bruite, size=(1, 5, 5))
    (_fig, _ax) = plt.subplots(1, 3, figsize=(12, 4))
    for (_a, im, title) in zip(_ax, (bruite, filtre_moyen_np, filtre_median_np), ('Bruitée', 'Filtre moyen', 'Filtre médian')):
        _a.imshow(im.transpose(1, 2, 0).astype('uint8'))
        _a.set_title(title)
        _a.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La **morphologie mathématique** applique plutôt des opérateurs ensemblistes (érosion, dilatation) à l'aide d'un élément structurant. L'**ouverture** (érosion puis dilatation) élimine les petits objets clairs isolés sans trop déformer les grandes structures, ce qui est utile pour nettoyer un masque binaire issu d'un seuillage ou d'une segmentation [@richards2022remote] :
    """)
    return


@app.cell
def _(img_SAR, np, plt):
    from skimage.morphology import opening, disk
    sar_db = np.log10(img_SAR.sel(band=1).to_numpy())
    masque = sar_db > np.percentile(sar_db, 75)
    masque_ouvert = opening(masque, disk(2))  # 25 % des pixels les plus intenses
    (_fig, _ax) = plt.subplots(1, 2, figsize=(8, 4))
    _ax[0].imshow(masque, cmap='gray')
    _ax[0].set_title('Masque original')
    _ax[1].imshow(masque_ouvert, cmap='gray')
    _ax[1].set_title('Après ouverture')
    [_a.axis('off') for _a in _ax]
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Gestion des bordures

    L'application de filtres à l'intérieur de fenêtres glissantes implique de gérer les bords de l'image, car la fenêtre de traitement va nécessairement déborder de quelques pixels en dehors de l'image (généralement la moitié de la fenêtre déborde). On peut soit décider d'ignorer les valeurs en dehors de l'image en imposant une valeur `nan`, soit prolonger l'image de quelques lignes et colonnes avec des valeurs miroirs ou constantes.

    #### Filtrage par une couche convolutionnelle

    **Installation de Pytorch**

    Cette section utilise la librairie PyTorch. Le calcul s'exécute très bien sur CPU (c'est le cas lors de la génération de ce livre) ; un GPU, par exemple sur Colab, ne fait que l'accélérer. Pour une installation locale en version CPU : `pip install -qU torch==2.4.0+cpu`

    Une couche convolutionnelle est simplement un ensemble de filtres appliqués sur la donnée d'entrée. Ce type de filtrage est à la base des réseaux dits convolutionnels qui seront abordés dans le tome 2. On peut ici imposer les mêmes filtres de gradient dans la couche convolutionnelle :
    """)
    return


@app.cell
def _(img_rgb, np, plt):
    import torch
    import torch.nn as nn
    normalized_img = torch.tensor(img_rgb.to_numpy())
    nchannels = normalized_img.size()[0]
    conv_layer = nn.Conv2d(in_channels=nchannels, out_channels=2, kernel_size=3, padding=1, stride=1, dilation=1)
    scharr_x = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    scharr_y = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])
    _kernel = np.stack([scharr_x, scharr_y])
    _kernel = _kernel.reshape(2, 1, 3, 3)
    _kernel = np.tile(_kernel, (1, nchannels, 1, 1))
    print(_kernel.shape)
    _kernel = torch.as_tensor(_kernel, dtype=torch.float32)
    conv_layer.weight = nn.Parameter(_kernel)
    conv_layer.bias = nn.Parameter(torch.zeros(2))
    input = normalized_img.unsqueeze(0)
    print(input.shape)
    (_fig, _axs) = plt.subplots(1, 2, figsize=(8, 5))
    for _i in range(2):
        _axs[_i].imshow(conv_layer.weight.data.numpy()[_i, 0])
        _axs[_i].set_title(f'Filtre {_i + 1}')
    plt.show()
    return conv_layer, input


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le résultat est alors calculé sur GPU (si disponible):
    """)
    return


@app.cell
def _(conv_layer, input, plt):
    output = conv_layer(input)
    print(f'Image (BxCxHxW): {input.shape}')
    print(f'Sortie (BxFxHxW): {output.shape}')
    (_fig, _axs) = plt.subplots(1, 2, figsize=(20, 5))
    for _i in range(2):
        _axs[_i].imshow(output.detach().data.numpy()[0, _i], vmin=-5000, vmax=5000, cmap='gray')
        _axs[_i].set_title(f'Filtrage {_i + 1}')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtrage adaptatif

    Les filtrages adaptatifs consistent à appliquer un traitement en fonction du contenu local d'une image. Le filtre n'est alors plus stationnaire et sa réponse peut varier en fonction du contenu local. Ce type de filtre est très utilisé pour filtrer les images SAR (Synthetic Aperture Radar) qui sont dégradées par un bruit multiplicatif que l'on appelle *speckle*. On peut voir un exemple d'une image Sentinel-1 (bande HH) sur la région de Montréal, remarquez que l'image est affichée en dB en appliquant la fonction `log10`.
    """)
    return


@app.cell
def _(img_SAR, plt, xr):
    print(img_SAR.rio.resolution())
    print(img_SAR.rio.crs)
    (_fig, _axs) = plt.subplots(1, 1, figsize=(6, 4))
    # imshow (raster) plutôt que .plot() (pcolormesh vectoriel = PDF de 40 Mo)
    xr.ufuncs.log10(img_SAR.sel(band=1).drop('band')).plot.imshow()
    _axs.set_title('Image SAR Sentinel-1 (dB)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Un des filtres les plus simples pour réduire le bruit est d'appliquer un filtre moyen, par exemple un $5 \times 5$ ci-dessous:
    """)
    return


@app.cell
def _(img_SAR, plt, xr):
    rolling_win_1 = img_SAR.sel(band=1).rolling(x=5, y=5, min_periods=3, center=True).construct(x='x_win', y='y_win', keep_attrs=True)
    filtre_moyen_1 = rolling_win_1.mean(dim=['x_win', 'y_win'], skipna=True)
    (_fig, _axs) = plt.subplots(1, 1, figsize=(6, 4))
    xr.ufuncs.log10(filtre_moyen_1).plot.imshow()
    _axs.set_title('Filtrage moyen 5x5 (dB)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Au lieu d'appliquer un filtre moyen de manière indiscriminée, le filtre de Lee [@Lee-1986] applique une pondération en fonction du contenu local de l'image $I$ dans sa forme la plus simple :

    $$
    \begin{aligned}
    I_F & = I_M + K \times (I - I_M) \\
    K & = \frac{\sigma^2_I}{\sigma^2_I + \sigma^2_{bruit}}
    \end{aligned}
    $$ {#eq-lee-filter}

    De la sorte, si la variance locale est élevée $K$ s'approche de $1$ préservant ainsi les détails de l'image $I$ sinon l'image moyenne $I_M$ est appliquée.

    En pratique, on exprime souvent la pondération $K$ à l'aide du **coefficient de variation** local $CV = \sigma_I / I_M$ : $K = (CV - CV_{bruit})\,/\,CV$, où $CV_{bruit}$ est le coefficient de variation du *speckle* (ici supposé $\approx 0{,}25$). C'est cette forme équivalente qui est utilisée dans le code ci-dessous (`ponderation`).
    """)
    return


@app.cell
def _(img_SAR, plt):
    rolling_win_2 = img_SAR.sel(band=1).rolling(x=5, y=5, min_periods=3, center=True).construct(x='x_win', y='y_win', keep_attrs=True)
    filtre_moyen_2 = rolling_win_2.mean(dim=['x_win', 'y_win'], skipna=True)
    ecart_type = rolling_win_2.std(dim=['x_win', 'y_win'], skipna=True)
    cv = ecart_type / filtre_moyen_2
    ponderation = (cv - 0.25) / cv
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4), sharex=True, sharey=True)
    plt.subplot(1, 2, 1)
    cv.plot.imshow(vmin=0, vmax=2)
    _axes[0].set_title('CV')
    plt.subplot(1, 2, 2)
    ponderation.plot.imshow(vmin=0, vmax=1)
    _axes[1].set_title('Pondération')
    plt.tight_layout()
    return filtre_moyen_2, ponderation


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On zoomant sur l'image, on voit clairement que les détails de l'image sont mieux préservés :
    """)
    return


@app.cell
def _(filtre_moyen_2, img_SAR, plt, ponderation, xr):
    filtered = filtre_moyen_2 + ponderation * (img_SAR.sel(band=1).drop('band') - filtre_moyen_2)
    (_fig, _axes) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4), sharex=True, sharey=True)
    plt.subplot(1, 2, 1)
    xr.ufuncs.log10(filtre_moyen_2).isel(x=slice(None, 250), y=slice(None, 250)).plot.imshow()
    _axes[0].set_title('Filtre moyen')
    plt.subplot(1, 2, 2)
    xr.ufuncs.log10(filtered).isel(x=slice(None, 250), y=slice(None, 250)).plot.imshow()
    _axes[1].set_title('Filtre de Lee')
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Texture (matrice de co-occurrence)

    Au-delà des contours, la **texture** — la façon dont les valeurs de gris varient spatialement — est une source d'information à part entière, en particulier pour distinguer des surfaces de radiométrie moyenne semblable mais d'organisation spatiale différente (p. ex. forêt versus champ). La **matrice de co-occurrence des niveaux de gris** (*Gray-Level Co-occurrence Matrix*, GLCM) compte, pour une direction et une distance données, la fréquence des paires de valeurs de gris voisines ; on en dérive ensuite des mesures statistiques comme le contraste, l'homogénéité, l'énergie et la corrélation [@Jensen2016; @richards2022remote]. On compare ci-dessous ces mesures sur deux fenêtres de `img_rgb` de contenu différent :
    """)
    return


@app.cell
def _(img_rgb, rgb2gray):
    from skimage.feature import graycomatrix, graycoprops
    from skimage.util import img_as_ubyte

    gris = img_as_ubyte(rgb2gray(img_rgb.to_numpy().transpose(1, 2, 0) / 255.0))

    fenetre_a = gris[:80, :80]     # coin supérieur gauche
    fenetre_b = gris[-80:, -80:]   # coin inférieur droit

    for nom, fenetre in [("Fenêtre A", fenetre_a), ("Fenêtre B", fenetre_b)]:
        glcm = graycomatrix(fenetre, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        proprietes = {p: graycoprops(glcm, p)[0, 0] for p in ("contrast", "homogeneity", "energy", "correlation")}
        print(nom, proprietes)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ces propriétés peuvent être ajoutées comme colonnes supplémentaires au tableau `regionprops_table` de la section suivante, pour enrichir la description de chaque segment au-delà de sa seule couleur moyenne.

    Ces mesures de texture reposent, comme la matrice de covariance de l'ACP (@sec-chap03), sur une statistique du second ordre calculée localement ; une description plus riche du voisinage — par exemple pour du filtrage anisotrope préservant les contours — passe par le **tenseur de structure**, qui encode à la fois l'orientation et l'intensité locale du gradient [@AjaFernandez-2009].

    ## Segmentation

    La segmentation d'image consiste à séparer une image en régions homogènes spatialement connexes (segments) où les valeurs sont uniformes selon un certain critère (couleurs, texture, etc.). Une image présente généralement beaucoup de pixels redondants, l'intérêt de ce type de méthode est essentiellement de réduire la quantité de pixels nécessaire. En télédétection, on parle souvent d'approche objet. En vision par ordinateur, on parle parfois de super-pixel. Il existe de nombreuses méthodes de segmentation, la librairie `sickit-image` rend disponible plusieurs implémentations sur des images RVB ([Comparison of segmentation and superpixel algorithms — skimage 0.25.0 documentation](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_segmentations.html#sphx-glr-auto-examples-segmentation-plot-segmentations-py)).

    ### Super-pixel

    Ce type de méthode cherche à former des régions homogènes et compactes dans l'image [@Achanta-2012]. Une des méthodes les plus simples est la méthode SLIC (*Simple Linear Iterative Clustering*), elle combine un regroupement de type k-moyennes avec une distance hybride qui prend en compte les différences de couleur entre pixels mais aussi leur distance par rapport centre du super-pixel:

    1.  Décomposer l'image en N régions régulières de taille $S \times S$

    2.  Initialiser les centres $C_k$ de chaque segment $k$

    3.  Rechercher les pixels ayant la distance la plus petite dans une région $2S \times 2S$:

    $$
    D_{SLIC}= d_{couleur} + \frac{m}{S}d_{xy}
    $$

    4.  Mettre à jour les centre $C_k$ de chaque segment $k$ et réitérer à l'étape 3.

    Les régions évoluent rapidement avec les itérations, plus le poids $m$ est élevé, plus la forme du super-pixel est contrainte et ne suivra pas vraiment le contenu de l'image:
    """)
    return


@app.cell
def _(img_rgb, mark_boundaries, np, plt, slic):
    img = img_rgb.to_numpy().astype('uint8').transpose(1, 2, 0)
    segments_slic1 = slic(img, n_segments=250, compactness=10, sigma=1, start_label=1, max_num_iter=1)
    segments_slic2 = slic(img, n_segments=250, compactness=10, sigma=1, start_label=1, max_num_iter=2)
    segments_slic100 = slic(img, n_segments=250, compactness=100, sigma=1, start_label=1, max_num_iter=10)
    segments_slic100b = slic(img, n_segments=250, compactness=10, sigma=1, start_label=1, max_num_iter=10)
    print(f'SLIC nombre de segments: {len(np.unique(segments_slic1))}')
    (_fig, _ax) = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)
    _ax[0, 0].imshow(mark_boundaries(img, segments_slic1))
    _ax[0, 0].set_title('Initialisation')
    _ax[0, 1].imshow(mark_boundaries(img, segments_slic2))
    _ax[0, 1].set_title('2 itérations')
    _ax[1, 0].imshow(mark_boundaries(img, segments_slic100))
    _ax[1, 0].set_title('10 itérations avec m=100')
    _ax[1, 1].imshow(mark_boundaries(img, segments_slic100b))
    _ax[1, 1].set_title('10 itérations avec m=10')
    for _a in _ax.ravel():
        _a.set_axis_off()
    plt.tight_layout()
    plt.show()
    return (img,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le nombre de segments initial est probablement le paramètre le plus important. Une manière de l'estimer est d'évaluer l'échelle moyenne des segments homogènes dans l'image à analyser. On observe ci-dessous l'impact de passer d'une échelle 40 x 40 à 20 x 20. En prenant la moyenne de chaque segment, on constate que l'échelle 40 x 40 génère des segments trop grands mélangeant plusieurs classes.
    """)
    return


@app.cell
def _(color, img, np, plt, segmentation, slic):
    n_regions = int(img.shape[0] * img.shape[1] / (40 * 40))
    print('Nb segments: ', n_regions)
    segments_slic_40 = slic(img, n_segments=n_regions, compactness=10, sigma=1, start_label=1, max_num_iter=10)
    print(f'SLIC nombre de segments: {len(np.unique(segments_slic_40))}')
    out = color.label2rgb(segments_slic_40, img, kind='avg', bg_label=0)
    out_40 = segmentation.mark_boundaries(out, segments_slic_40, (0, 0, 0))
    n_regions = int(img.shape[0] * img.shape[1] / (20 * 20))
    print('Nb segments: ', n_regions)
    segments_slic_20 = slic(img, n_segments=n_regions, compactness=10, sigma=1, start_label=1, max_num_iter=10)
    print(f'SLIC nombre de segments: {len(np.unique(segments_slic_20))}')
    out = color.label2rgb(segments_slic_20, img, kind='avg', bg_label=0)
    out_20 = segmentation.mark_boundaries(out, segments_slic_20, (0, 0, 0))
    (_fig, _ax) = plt.subplots(2, 1, figsize=(6, 8), sharex=True, sharey=True)
    _ax[0].imshow(out_40)
    _ax[0].set_title('Initialisation avec 631 segments')
    _ax[1].imshow(out_20)
    _ax[1].set_title('Initialisation avec 2526 segments')
    for _a in _ax.ravel():
        _a.set_axis_off()
    plt.tight_layout()
    plt.show()
    return (segments_slic_20,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quick Shift

    Le *Quick Shift* est une autre méthode de segmentation par recherche de mode (*mode seeking*), fonctionnant par ascension de gradient vers le voisin le plus proche de densité supérieure dans un espace couleur-position combiné, plutôt que par les k-moyennes itératives de SLIC [@Vedaldi-2008]. Elle ne requiert pas de fixer à l'avance le nombre de segments, mais plutôt une échelle spatiale (`kernel_size`) et une distance maximale de fusion (`max_dist`) :
    """)
    return


@app.cell
def _(img, mark_boundaries, np, plt, segments_slic_20):
    from skimage.segmentation import quickshift
    segments_qs = quickshift(img, kernel_size=5, max_dist=10, ratio=0.5)
    print(f'Quick Shift nombre de segments: {len(np.unique(segments_qs))}')
    (_fig, _ax) = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)
    _ax[0].imshow(mark_boundaries(img, segments_slic_20))
    _ax[0].set_title(f'SLIC ({len(np.unique(segments_slic_20))} segments)')
    _ax[1].imshow(mark_boundaries(img, segments_qs))
    _ax[1].set_title(f'Quick Shift ({len(np.unique(segments_qs))} segments)')
    [_a.axis('off') for _a in _ax]
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le paramètre `ratio` (entre 0 et 1) équilibre l'importance de la couleur par rapport à la position spatiale, un rôle analogue au poids $m$ de SLIC.

    ### Fusion des segments par graphe de proximité

    Une segmentation peut produire beaucoup trop de segments. On parle alors de sur-segmentation. Ceci est recherché dans certains cas pour permettre de bien capturer les détails fins de l'image. Cependant, afin de réduire le nombre de segments, un post-traitement possible est de fusionner les segments similaires selon certaines règles ou distances. Un graphe d'adjacence de régions (@fig-rag) est formé à partir des segments connectés où chaque nœud représente un segment et un lien de proximité (@Jaworek-2018). À partir de ce graphe, on peut fusionner les nœuds similaires à partir de leur distance radiométrique.
    """)
    return


@app.cell
def _(color, graph, img, np, plt, segmentation, segments_slic_20):
    def _weight_mean_color(graph, src, dst, n):
        """Fonction pour gérer la fusion des nœuds en recalculant la couleur moyenne.
        La méthode suppose que la couleur moyenne de `dst` est déjà calculée.
        """
        diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
        diff = np.linalg.norm(diff)
        return {'weight': diff}

    def merge_mean_color(graph, src, dst):
        """Fonction appelée avant la fusion de deux nœuds d'un graphe de distance de couleur moyenne.
          Cette méthode calcule la couleur moyenne de `dst`.
        """
        graph.nodes[dst]['total color'] = graph.nodes[dst]['total color'] + graph.nodes[src]['total color']
        graph.nodes[dst]['pixel count'] = graph.nodes[dst]['pixel count'] + graph.nodes[src]['pixel count']
        graph.nodes[dst]['mean color'] = graph.nodes[dst]['total color'] / graph.nodes[dst]['pixel count']
    g = graph.rag_mean_color(img, segments_slic_20)
    print('Nombre de segments:', len(g))
    labels2 = graph.merge_hierarchical(segments_slic_20, g, thresh=20, rag_copy=False, in_place_merge=True, merge_func=merge_mean_color, weight_func=_weight_mean_color)
    print('Nombre de segments:', len(g))
    out1 = color.label2rgb(segments_slic_20, img, kind='avg', bg_label=0)
    out1 = segmentation.mark_boundaries(out1, segments_slic_20, (0, 0, 0))
    out2 = color.label2rgb(labels2, img, kind='avg', bg_label=0)
    out2 = segmentation.mark_boundaries(out2, labels2, (0, 0, 0))
    (_fig, _ax) = plt.subplots(nrows=2, sharex=True, sharey=True, figsize=(6, 8))
    _ax[0].imshow(out1)
    _ax[0].set_title('Avant fusion')
    _ax[1].imshow(out2)
    _ax[1].set_title('Après fusion')
    for _a in _ax:
        _a.axis('off')
    plt.tight_layout()
    return (labels2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Approche objet

    L'approche objet consiste à traiter chaque segment comme un objet avec un ensemble de propriétés. La librairie `skimage` offre la possibilité d'enrichir chaque segment avec des [propriétés](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops) et de former un tableau:
    """)
    return


@app.cell
def _(img_rgb, labels2, measure, pd):
    properties = ['label', 'area', 'centroid', 'num_pixels', 'intensity_mean', 'intensity_std']

    table=   measure.regionprops_table(labels2, intensity_image= img_rgb.to_numpy().transpose(1,2,0), properties=properties)

    table = pd.DataFrame(table)
    table.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ce tableau pourra être exploiter pour une tâche de classification par la suite (on parle alors de classification objet).

    ## Points clés

    ## Exercices

    **À vous de jouer**

    1.  Décimez `img_rgb` par un facteur 8, **avec** et **sans** filtre passe-bas gaussien préalable, et comparez l'aliasing obtenu.

    2.  Appliquez le filtre de Scharr sur les **trois bandes** RVB (plutôt qu'une seule) et combinez les amplitudes de gradient (p. ex. la norme euclidienne).

    3.  Faites varier la taille de la fenêtre (3×3, 7×7, 11×11) du filtre de Lee sur `img_SAR` et observez l'effet sur la préservation des détails.

    4.  Reprenez SLIC avec plusieurs valeurs de `compactness` (1, 10, 50) et décrivez l'effet sur la forme des super-pixels.

    5.  *(filtrage non linéaire)* Comparez un filtre médian et un filtre moyen de même taille sur une image bruitée par du bruit impulsionnel (*sel et poivre*) et discutez la préservation des contours.

    6.  *(texture)* Calculez les propriétés GLCM (contraste, homogénéité, énergie, corrélation) sur deux fenêtres de `img_SAR` (en dB) de contenu différent et comparez-les à celles obtenues sur `img_rgb`.

    7.  *(Quick Shift)* Faites varier `kernel_size` et `max_dist` de Quick Shift sur `img_rgb` et comparez le nombre de segments obtenus à celui de SLIC.

    ## Quiz

    ::: {.content-visible when-profile="production"}

    Utilisez la version html.
    :::
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz
    Chap04Quiz = Quiz("quiz/Chap04.yml", "Chap04")
    render_quizz(Chap04Quiz)
    return


if __name__ == "__main__":
    app.run()
