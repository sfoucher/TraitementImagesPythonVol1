# /// script
# dependencies = ["rioxarray", "xrscipy"]
# ///

import marimo

__generated_with = "0.23.15"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Importation et manipulation de données spatiales {#sec-chap01}

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous abordons quelques formats d'images ainsi que leur lecture. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/01-ImportationManipulationImages.ipynb)

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">

    </div>
    </div>

    ### Bibliothèques

    Les bibliothèques qui vont être explorées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [opencv-python · PyPI](https://pypi.org/project/opencv-python/)

    -   [scikit-image](https://scikit-image.org/)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` et `gdal` doivent être installés:
    """)
    return


@app.cell
def _(subprocess):
    #! apt-get update
    subprocess.call(['apt-get', 'update'])
    #! apt-get install gdal-bin libgdal-dev
    subprocess.call(['apt-get', 'install', 'gdal-bin', 'libgdal-dev'])
    # packages added via marimo's package management: rioxarray xrscipy !pip install -q rioxarray xrscipy
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifier les importations:
    """)
    return


@app.cell
def _():
    import numpy as np
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import xrscipy
    import matplotlib.pyplot as plt

    return np, plt, rxr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Données

    Nous utilisons ces images dans ce chapitre:
    """)
    return


@app.cell
def _(subprocess):
    import gdown

    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6Ypg0g1Oy4AJt9XWKWfnR12NW1XhNg_', output= 'RGBNIR_of_S2A.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a4PQ68Ru8zBphbQ22j0sgJ4D2quw-Wo6', output= 'landsat7.tif')
    gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    #! wget https://raw.githubusercontent.com/sfoucher/TraitementImagesPythonVol1/refs/heads/main/images/modis-aqua.PNG -O modis-aqua.PNG
    subprocess.call(['wget', 'https://raw.githubusercontent.com/sfoucher/TraitementImagesPythonVol1/refs/heads/main/images/modis-aqua.PNG', '-O', 'modis-aqua.PNG'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Vérifiez que vous êtes capable de les lire:
    """)
    return


@app.cell
def _(rxr):
    with rxr.open_rasterio('berkeley.jpg', mask_and_scale=True) as _img_rgb:
        print(_img_rgb)
    with rxr.open_rasterio('RGBNIR_of_S2A.tif', mask_and_scale=True) as img_rgbnir:
        print(img_rgbnir)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Importation d'images

    La première étape avant tout traitement est d'accéder à la donnée image pour qu'elle soit manipulée par le langage Python. L'imagerie satellite présente certains défis notamment en raison de la taille parfois très importante des images. Il existe maintenant certaines bibliothèques, comme [Xarray](https://docs.xarray.dev/en/stable/), qui visent à optimiser la lecture et l'écriture de grandes images. Il est donc conseillé de toujours garder un oeil sur l'espace mémoire occupé par les variables Python représentant les images. La librairie principale en géomatique qui permettre d'importer (et d'exporter) de l'imagerie est la librairie [GDAL](https://gdal.org) qui rassemble la plupart des formats sous forme de *driver* (ou pilote en français).

    Dans le domaine de la géomatique, il faut prêter attention à quatre caractéristiques principales des images:

    1\. **La matrice des données** elle-même qui contient les valeurs brutes des pixels. Cette matrice sera souvent un cube à trois dimensions. En Python, ce cube sera le plus souvent un objet de la librairie [NumPy](https://numpy.org/) (voir la section « Manipulation de la matrice de pixels » plus bas).

    2\. **La dynamique des images** c.-à.-d le format de stockage des valeurs individuelles (octet, entier, double, etc.). Ce format décide principalement de la résolution radiométrique et des valeurs minimales et maximales supportées.

    3\. **Le nombre de bandes** spectrales de l'image qui est souvent supérieur à trois et peut atteindre plusieurs centaines de bandes pour certains capteurs (notamment hyperspectraux).

    4\. **La métadonnée** qui va transporter l'information auxiliaire de l'image comme les dimensions et la position de l'image, la date, etc. Cette donnée auxiliaire prendra souvent la forme d'un dictionnaire Python. Elle contiendra aussi l'information de géoréférence.

    Les différents formats se distinguent principalement sur la manière dont ces quatre caractéristiques sont gérées.

    ### Formats des images

    Il existe de nombreux formats numériques pour la donnée de type image parfois appelé donnée matricielle ou donnée *raster*. La librairie GDAL rassemble la plupart des formats matriciels rencontrés en géomatique (voir [Raster drivers — GDAL documentation](https://gdal.org/en/latest/drivers/raster/index.html) pour une liste complète).

    On peut distinguer deux grandes familles de format:

    1\. Les formats de type **RVB** issus de l'imagerie numérique grand public comme [JPEG](https://gdal.org/en/latest/drivers/raster/jpeg.html#raster-jpeg), [png](https://gdal.org/en/latest/drivers/raster/png.html#raster-png), etc. Ces formats ne supportent généralement que trois bandes au maximum (rouge, vert et bleu) et des valeurs de niveaux de gris entre 0 et 255 (format dit 8 bits ou `uint8`).

    2\. **Les géo-formats** issus des domaines scientifiques ou techniques comme GeoTIFF, HDF5, NetCDF, etc. qui peuvent inclure plus que trois bandes et des dynamiques plus élevées (16 bits ou même float).

    Les formats RVB restent très utilisés en Python notamment par les bibliothèques dites de vision par ordinateur (*Computer Vision*) comme OpenCV et scikit-image ainsi que les grandes bibliothèques en apprentissage profond (PyTorch, Tensorflow).

    <div style="border:0.5px solid silver;border-left:.3rem solid #352c76;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2e1f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAABhUlEQVRYhe2Wv3HCMByFP3P0YYMwQHShiGrYgGSCsEFcRSWmVBWYIGYDNoDUashpAdiATOAUyMZnDvsiMKTwa2z9ud/7znqSFSRJQlFSqA1wfzRwnrbG6m6xMygCSKEiYAx8AauKoiP3jCvmDYA+MDFWRycBpFBdYO2aPWP1pqyqFGoFYKweVMw7WbdVmDsF7oBplflf5GpltfNjGYAUagAM2a9VdCnzHEQEbIGh8zoASKE6HNZxdGnznNLasfPMvkDIPvVzY/WqLndXe+68QoCWC8gY+Ek7a1bovMZSqG7w9PAeOYBbaNLONb6B3ZWMO8AjQB4grHP983K7YAnH58DV1a6aIIUa4b81Y2N17A0ghXoGPj3NAfpSqJ2xeuEFAPQAjNWBj7sUKnE1TgL8/wxAltqbAKS/0OUZHuuywVIAY/VCCvWCy4KPeVkAKwFSCEpCdK5uHsIGoAFoABqAPIDvceujzKvN4Wfx4a7odV9MO8Cbe18HSZIghYqB15qNi5oZq8Nf0ER+TJGyROAAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Installation de gdal dans un système Linux</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li>Pour installer GDAL :</li>
    </ul>
    <pre><code>!apt-get update
    !apt-get install gdal-bin libgdal-dev</code></pre>
    </div>
    </div>

    #### Formats de type RVB

    Les premiers formats pour de l'imagerie à une bande (monochrome) et à trois bandes (image couleur rouge-vert-bleu) sont issus du domaine des sciences de l'ordinateur. On trouvera, entre autres, les formats pbm, png et jpeg. Ces formats supportent peu de métadonnées et sont placées dans un entête (*header*) très limité. Cependant, ils restent très populaires dans le domaine de la vision par ordinateur et sont très utilisés en apprentissage profond en particulier. Pour la lecture des images RVB, on peut utiliser les bibliothèques Rasterio, [PIL](https://he-arc.github.io/livre-python/pillow/index.html) ou [OpenCV](https://docs.opencv.org/4.10.0/index.html).

    ##### Lecture avec la librairie PIL

    La librairie PIL retourne un objet de type `PngImageFile`, l'affichage de l'image se fait directement dans la cellule de sortie.
    """)
    return


@app.cell
def _():
    from PIL import Image
    _img = Image.open('modis-aqua.PNG')
    _img
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Lecture avec la librairie OpenCV

    La librairie [OpenCV](https://docs.opencv.org/4.10.0/index.html) est aussi très populaire en vision par ordinateur. La fonction `imread` donne directement un objet de type NumPy en sortie.
    """)
    return


@app.cell
def _():
    import cv2
    _img = cv2.imread('modis-aqua.PNG')
    _img
    return (cv2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Attention : la fonction `imread` d'OpenCV renvoie les canaux dans l'ordre **BGR** (bleu, vert, rouge) et non RGB. Il faut convertir l'image avant de l'afficher correctement avec `matplotlib` :
    """)
    return


@app.cell
def _(cv2, plt):
    img_bgr = cv2.imread('modis-aqua.PNG')
    _img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    (fig, ax) = plt.subplots(1, 2, figsize=(8, 4))
    ax[0].imshow(img_bgr)
    ax[0].set_title('Sans conversion (BGR)')
    ax[0].axis('off')
    ax[1].imshow(_img_rgb)
    ax[1].set_title('Après conversion (RGB)')
    ax[1].axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Lecture avec la librairie RasterIO

    Rien ne nous empêche de lire une image de format RVB avec [RasterIO](https://rasterio.readthedocs.io/en/stable/) comme décrit dans ci-dessous. Vous noterez cependant les avertissements concernant l'absence de géoréférence pour ce type d'image.
    """)
    return


@app.cell
def _():
    import rasterio
    _img = rasterio.open('modis-aqua.PNG')
    _img
    return (rasterio,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Le format GeoTiff

    Le format GeoTIFF est une extension du format TIFF (Tagged Image File Format) qui permet d'incorporer des métadonnées géospatiales directement dans un fichier image. Développé initialement par Dr. Niles Ritter au Jet Propulsion Laboratory de la [NASA](https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/geotiff){target="_blank"} dans les années 1990, GeoTIFF est devenu un standard de facto pour le stockage et l'échange d'images géoréférencées dans les domaines de la télédétection et des systèmes d'information géographique (SIG). Ce format supporte plus que trois bandes aussi longtemps que ces bandes sont de même dimension.

    Le format GeoTIFF est très utilisé et est largement supporté par les bibliothèques et logiciels géospatiaux, notamment [GDAL](https://gdal.org) (*Geospatial Data Abstraction Library*), qui offre des capacités de lecture et d'écriture pour ce format. Cette compatibilité étendue a contribué à son adoption généralisée dans la communauté géospatiale.

    ##### Standardisation par l'OGC

    Le standard GeoTIFF proposé par l'Open Geospatial Consortium (OGC) en 2019 formalise et étend les spécifications originales du format GeoTIFF, offrant une norme robuste pour l'échange d'images géoréférencées. Cette standardisation, connue sous le nom d'OGC GeoTIFF 1.1 [-@OGCGeoTIFF], apporte plusieurs améliorations et clarifications importantes.

    #### Le format COG

    Une innovation récente dans l'écosystème GeoTIFF est le format *Cloud Optimized GeoTIFF* ([COG](http://cogeo.org/)), conçu pour faciliter l'utilisation de fichiers GeoTIFF hébergés sur des serveurs web HTTP. Le COG permet aux utilisateurs et aux logiciels d'accéder à des parties spécifiques du fichier sans avoir à le télécharger entièrement, ce qui est particulièrement utile pour les applications basées sur l'infonuagique.

    ### Métadonnées des images

    La manière la plus directe d'accéder à la métadonnée d'une image est d'utiliser les commandes [`rio info`](https://rasterio.readthedocs.io/en/stable/cli.html#info) de la librairie Rasterio ou `gdalinfo` de la librairie `gdal`. Le résultat est imprimé dans la sortie standard ou sous forme d'un dictionnaire Python.
    """)
    return


@app.cell
def _(subprocess):
    #! gdalinfo RGBNIR_of_S2A.tif
    subprocess.call(['gdalinfo', 'RGBNIR_of_S2A.tif'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le plus simple est d'utiliser la fonction `rio info`:
    """)
    return


@app.cell
def _(subprocess):
    #! rio info RGBNIR_of_S2A.tif --indent 2 --verbose
    subprocess.call(['rio', 'info', 'RGBNIR_of_S2A.tif', '--indent', '2', '--verbose'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Depuis Python, `rasterio` donne accès à ces mêmes informations sous forme d'attributs et d'un dictionnaire de métadonnées :
    """)
    return


@app.cell
def _(rasterio):
    with rasterio.open('RGBNIR_of_S2A.tif') as src:
        print('Nombre de bandes :', src.count)
        print('Dimensions (lignes, colonnes) :', src.height, src.width)
        print('Type des pixels :', src.dtypes[0])
        print('Système de coordonnées :', src.crs)
        print('Résolution (m) :', src.res)
        print('Emprise :', src.bounds)
        meta = src.meta
    meta  # toutes les métadonnées dans un dictionnaire
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Manipulation des images

    ### Manipulation de la matrice de pixels

    La donnée brute de l'image est généralement contenue dans un cube matricielle à trois dimensions (deux dimensions spatiales et une dimension spectrale). Comme exposé précédemment, la librairie dite *"fondationnelle"* pour la manipulation de matrices en Python est [NumPy](https://numpy.org/). Cette librairie contient un nombre très important de fonctionnalités couvrant l'algèbre linéaire, les statistiques, etc.; elle constitue la fondation de nombreuses bibliothèques en traitement numérique (voir (@fig-naturenumpy1))

    ![La librairie NumPy est le fondement de nombreuses bibliothèques scientifiques (d'après [@NumpyNature]).](images/41586_2020_2649_Fig2_HTML.png){#fig-naturenumpy1 width="100%" fig-align="center"}

    ### Information de base

    Les deux informations de base à afficher sur une matrice sont 1) les dimensions de la matrice et 2) le format de stockage (le type). Pour cela, on peut utiliser le code ci-dessous, dont le résultat nous informe que la matrice a trois dimensions et une taille de `(442, 553, 3)` et un type `uint8` qui représente 1 octet (8 bit). Par conséquent, la matrice a `442` lignes, `553` colonnes et `3` canaux ou bandes. Il faut prêter une attention particulière aux valeurs minimales et maximales tolérées par le type de la donnée comme indiqué dans le (@tbl-numpytype) (voir aussi [Data types — NumPy v2.1 Manual](https://numpy.org/doc/stable/user/basics.types.html)).
    """)
    return


@app.cell
def _(cv2):
    _img = cv2.imread('modis-aqua.PNG')
    print('Nombre de dimensions: ', _img.ndim)
    print('Dimensions de la matrice: ', _img.shape)
    print('Type de la donnée: ', _img.dtype)
    return


@app.cell
def _():
    from IPython.display import Markdown
    from tabulate import tabulate
    table = [["uint8",   "unsigned char",  8,  0,           255],
             ["int8",    "signed char",    8, -128,         127],
             ["uint16",  "unsigned short", 16, 0,           65535],
             ["int16",   "short",          16, -32768,      32767],
             ["uint32",  "unsigned int",   32, 0,           4294967295],
             ["int32",   "int",            32, -2147483648, 2147483647],
             ["float32", "float",          32, "-3.4e38",   "3.4e38"],
             ["float64", "double",         64, "-1.8e308",  "1.8e308"]]
    Markdown(tabulate(table, headers=["dtype", "Nom", "Taille (bits)", "Min", "Max"], tablefmt="pipe"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Découpage et indexation de la matrice

    L'indexation et le découpage (*slicing*) des matrices dans NumPy sont des techniques essentielles pour manipuler efficacement les données multidimensionnelles en Python, offrant une syntaxe puissante et flexible pour accéder et modifier des sous-ensembles spécifiques d'éléments dans les tableaux (voir @fig-naturenumpy2). Indexer une matrice consiste à accéder à une valeur dans la matrice pour une position particulière, la syntaxe générale est `matrice[ligne, colonne, bande]` et est similaire à la manipulation des [listes](https://docs.python.org/fr/3/tutorial/introduction.html#lists) en Python. Les indices commencent à `0` et se termine à la `taille-1` de l'axe considéré.

    ![Vue d'ensemble des opérations de base des matrices avec NumPy](images/41586_2020_2649_Fig1_HTML.png){#fig-naturenumpy2 width="100%" fig-align="center"}

    Le découpage (ou *slicing* en anglais) consiste à produire une nouvelle matrice qui est un sous-ensemble de la matrice d'origine. Un découpage se fait avec le symbole ':', la syntaxe générale pour définir un découpage est `[début:fin:pas]`. Si on ne spécifie pas `début` ou `fin` alors les valeurs 0 ou `dimension-1` sont considérées implicitement. Quelques exemples :

    -   choisir un pixel en particulier avec toutes les bandes : `matrice[1, 1, :]`;
    -   choisir la troisième colonne (indice 2) avec toutes les bandes : `matrice[:, 2, :]`.

    La syntaxe de base pour le découpage (*slicing*) des tableaux NumPy repose sur l'utilisation des deux-points (`:`) à l'intérieur des crochets d'indexation. Cette notation permet de sélectionner des plages d'éléments de manière concise et intuitive. La structure générale du découpage est `matrice[start:stop:step]`, où : 1. `start` représente l'index de départ (inclus) 2. `stop` indique l'index de fin (exclu) 3. `step` définit l'intervalle entre chaque élément sélectionné

    Si l'un de ces paramètres est omis, NumPy utilise des valeurs par défaut : 0 pour `start`, la taille du tableau pour `stop`, et 1 pour `step`. Par exemple, pour un tableau unidimensionnel `array`, on peut extraire les éléments du deuxième au quatrième avec `array[1:4]`. Pour sélectionner tous les éléments à partir du troisième, on utiliserait `array[2:]`. Cette syntaxe s'applique également aux tableaux multidimensionnels, où chaque dimension est séparée par une virgule. Ainsi, pour une matrice 2D m, `m[0:2, 1:3]` sélectionnerait une sous-matrice 2x2 composée des deux premières lignes et des deuxième et troisième colonnes. L'indexation négative est également supportée, permettant de compter à partir de la fin du tableau. Par exemple, `a[-3:]` sélectionnerait les trois derniers éléments d'un tableau.
    """)
    return


@app.cell
def _(cv2):
    _img = cv2.imread('modis-aqua.PNG')
    img_col = _img[:, 1, :]
    print('Nombre de dimensions: ', img_col.ndim)
    print('Dimensions de la matrice: ', img_col.shape)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div style="border:0.5px solid silver;border-left:.3rem solid #eb5f23;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fef4ec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADSElEQVRYhbWX0W3bMBCGPwd5jwvwPUY1QNQJokxQL1DVmSDuBHEnqDNBFS7QdIJKE9QdgIDzXAFRJnAfeIzPDC05TXuAIZu64//z7ueRHm02G/63tWU2BvLUu+P/BFbIJwfO+/z/GYG2zApgBnyMXjXAWj7aZsDpqwkI8ILtSu+BCrgz1q0G4l5HoC2zJXAlPxtgYayrDwzPgaaXQFtmE2AKpFayBM7wK55p4LbMpmxFV8ekRCcnQLeXQFtmOVCL4z77LuCdiqvY1cF1W2Y3xrq5GivkuTraA14o8E/AhTxvlNutsW4agRcCfi/kGuARuJIFxQTqZxloy2wGfJWfl8a6SsZXQiqAzxLcw8RrY91U4mq8QHUppwDGul0CCvwRmEa1q/A13wc+ZJ1g5MApPkPbPqBq9wgUegu1ZTYH3gPNAPgdcA2ct2W2xu/9XL0DCFqoAEabzUaD/8KLSoNP2KZuomuesqiEyILmxrpK1L8GOmPdBOA4Um0NTGUb1YrxCV4PSXBJa2esWwtQjRKasW4t3xcy1zLEjn5/eNvRv9UA7gPjBPgCn/bPxrrFvgmE5M94rmNj3Vg5jKO4UPslCYt0c5fyEb8xUnO2GvAEwpdU35Z9/Z7oIJEJl2x1UwxoI3TNW2PdDtFkI1IWSFWhkQh4fSi4FnhqB42GLiRRb8jxqT4DbvHq3ifMsfie9xFNElA3mJWxrlNCC9bbjCRblRAFeLOP6LMSqBT/4HkTAdnXPeBziQ/g9JVoh4AwX0lwA6ykBLW4NET7WMfK/v8iQ5fif78PHFQJouP3KcVtmW3YrvpOre5Wxgp5hhtRg++maznAOmNdcUgGdsClFACf8QKqJJUFXlQfgQfgm4A3wIWxrlCd74wBO1Kr7/Bpmwvzh7bMCulueVtm67bMZopEI0QAbgS4DhNLOx+0Y3hqQhMlwDOZfNXuHi6d+HdAIY3qRxhX4Dom2UV3MqCyoAVY4A+P0AMu4y6WsqhvvBuKiTVwitdAAL9iez+oDgCvFHiRau9JArL6E3wtZ/JOgw9NVEd3ivwQcNjVwCh69w5/t+s7ZAp5VvjsHXIwPSeQskNXIBbueLOXgPcSeKH97UX11QSWJP75vMT+AHO9uY9+8Go9AAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>Une vue versus une copie</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    Avec NumPy, les manipulations peuvent créer des vues ou des copies. Une vue est une simple représentation de la même donnée originale alors qu’une copie est un nouvel espace mémoire.

    Par défaut, un découpage créé une vue.

    On peut vérifier si l’espace mémoire est partagé avec <code>np.shares_memory(arr, slice_arr)</code>.

    On peut toujours forcer une copie avec la méthode <code>copy()</code>

    </div>
    </div>

    ```{=html}

    ```

    ### Masquage

    L'utilisation d'un masque est un outil important en traitement d'image car la plupart des images de télédétection contiennent des pixels non valides qu'il faut exclure des traitements (ce que l'on appelle le *no data* en Anglais). Il y a plusieurs raison possibles pour la présence de pixels non valides:

    1.  L'image est projetée dans une grille cartographique et certaines zones, généralement situées en dehors de l'empreinte au sol du capteur, sont à exclure.

    2.  La présence de nuages que l'on veut exclure.

    3.  La présence de pixels erronés dus à des problèmes de capteurs.

    4.  La présence de valeurs non numériques (*not a number* ou `nan`)

    La librairie NumPy fournit des mécanismes pour exclure automatiquement certaines valeurs. Le module `numpy.ma` permet de créer un tableau masqué où les pixels non valides sont ignorés par les calculs statistiques :
    """)
    return


@app.cell
def _(np):
    _img = np.array([[12, 0, 15], [8, 20, 0], [0, 21, 23]], dtype=float)
    img_masque = np.ma.masked_equal(_img, 0)
    print('Moyenne sans masque :', round(_img.mean(), 2))
    print('Moyenne avec masque :', round(img_masque.mean(), 2))
    img_nan = np.where(_img == 0, np.nan, _img)
    print('Moyenne (nanmean)   :', round(np.nanmean(img_nan), 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Calcul d'un rapport de bandes

    Une opération très courante consiste à combiner deux bandes pixel par pixel. Par exemple, un rapport normalisé entre le proche-infrarouge et le rouge met en évidence la végétation (ce type d'indice spectral est approfondi au chapitre @sec-chap03) :
    """)
    return


@app.cell
def _(rxr):
    _img = rxr.open_rasterio('RGBNIR_of_S2A.tif').astype('float32')
    rouge = _img.sel(band=1)
    _pir = _img.sel(band=4)
    rapport = (_pir - rouge) / (_pir + rouge)
    print('Forme du rapport :', rapport.shape)
    print('Valeurs min/max  :', round(float(rapport.min()), 2), round(float(rapport.max()), 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exportation d'une image

    Une image chargée avec `rioxarray` peut être réécrite sur le disque au format GeoTIFF avec `rio.to_raster`, en conservant sa géoréférence :
    """)
    return


@app.cell
def _(rxr):
    _img = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    img_rvb = _img.sel(band=[1, 2, 3])
    img_rvb.rio.to_raster('RGBNIR_rvb.tif')
    print('Image exportée :', tuple(img_rvb.sizes.values()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Changement de projection cartographique

    Une image géoréférencée peut être reprojetée dans un autre système de coordonnées avec `rio.reproject`. `rioxarray` recalcule alors la grille de pixels et met à jour la géoréférence :
    """)
    return


@app.cell
def _(rxr):
    _img = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    print("CRS d'origine :", _img.rio.crs)
    img_wgs84 = _img.rio.reproject('EPSG:4326')
    print('Après reprojection :', img_wgs84.rio.crs)
    print('Nouvelle forme :', dict(img_wgs84.sizes))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```{=html}

    ```

    ## Données en géoscience

    Les données en géoscience contiennent beaucoup de métadonnées et peuvent être composées de différentes variables avec différentes unités, résolution, etc. Ces données sont aussi souvent étiquetées avec des dates sur certains axes, des coordonnées géographiques, des identifiants d'expériences, etc. Par conséquent, utiliser seulement des matrices est souvent incomplet [@xarray-2017].

    Calibration, unités, données manquantes, données éparses.

    ### xarray

    [Xarray](https://docs.xarray.dev/en/latest/getting-started-guide/why-xarray.html) est une puissante bibliothèque Python qui améliore les matrices multidimensionnelles de type numpy en y ajoutant des étiquettes, des dimensions, des coordonnées et des attributs. Elle fournit deux structures de données principales : `DataArray` (un tableau étiqueté à n dimensions) et `Dataset` (une base de données de tableaux multidimensionnels en mémoire).

    Les caractéristiques principales sont les suivantes:

    -   Opérations sur les dimensions nommées au lieu des numéros d'axe

    -   Sélection et opérations basées sur les étiquettes

    -   Diffusion automatique de tableaux basée sur les noms de dimensions

    -   Alignement de type base de données avec des étiquettes de coordonnées

    -   Suivi des métadonnées grâce à des dictionnaires Python

    #### Avantages

    La bibliothèque réduit considérablement la complexité du code et améliore la lisibilité du code pour les applications de calcul scientifique dans divers domaines, notamment la physique, l'astronomie, les géosciences, la bio-informatique, l'ingénierie, la finance et l'apprentissage profond. Elle s'intègre de manière transparente avec NumPy et pandas tout en restant compatible avec l'écosystème Python au sens large.

    #### DataArray

    Un tableau multidimensionnel étiqueté avec des propriétés clées :

    -   `valeurs` : Les données réelles du tableau

    -   `dims` : Dimensions nommées (par exemple, « x », « y », « z »)

    -   `coords` : Dictionnaire de tableaux étiquetant chaque point

    -   `attrs` : Stockage de métadonnées arbitraires

    -   `name` : Identifiant facultatif

    #### Dataset

    Un conteneur de type dictionnaire de `DataArrays` avec des dimensions alignées, contenant :

    -   `dims` : Dictionnaire de correspondance entre les noms des dimensions et les longueurs

    -   `data_vars` : Dictionnaire des variables du DataArray

    -   `coords` : Dictionnaire des variables de coordonnées

    -   `attrs` : Stockage des métadonnées

    Les principales différences sont les suivantes :

    -   `DataArray` contient un seul tableau avec des étiquettes

    -   Le `Dataset` contient plusieurs DataArrays alignés.

    Ces deux structures prennent en charge les opérations de type dictionnaire et les calculs de coordination tout en conservant les métadonnées.

    ![Organisation d'un Dataset dans xarray](images/xarray-dataset-diagram.png){#fig-xarray width="80%" fig-align="center"}

    #### Exemple avec rioxarray

    `rioxarray` ouvre un GeoTIFF directement comme un `DataArray` étiqueté : ses dimensions (`band`, `y`, `x`), ses coordonnées et sa géoréférence sont accessibles via l'accesseur `.rio`. On peut alors sélectionner une bande par son étiquette plutôt que par un numéro d'axe :
    """)
    return


@app.cell
def _(rxr):
    _img = rxr.open_rasterio('RGBNIR_of_S2A.tif')
    print('Dimensions :', dict(_img.sizes))
    print('Système de coordonnées :', _img.rio.crs)
    print('Résolution (m) :', _img.rio.resolution())
    _pir = _img.sel(band=4)
    print('Bande PIR — forme :', _pir.shape, '| valeur maximale :', int(_pir.max()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```{=html}

    ```

    ```{=html}

    ```

    ## Quiz

    ::: {.content-visible when-profile="production"}

    Utilisez la version html.
    :::
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz
    Chap01Quiz = Quiz("quiz/Chap01.yml", "Chap01")
    render_quizz(Chap01Quiz)
    return


if __name__ == "__main__":
    app.run()
