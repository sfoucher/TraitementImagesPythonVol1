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
    # Transformations spectrales {#sec-chap03}

    ## Préambule

    Assurez-vous de lire ce préambule avant d'exécuter le reste du notebook.

    ### Objectifs

    Dans ce chapitre, nous abordons l'exploitation de la dimension spectrale des images satellites. Ce chapitre est aussi disponible sous la forme d'un notebook Python:

    [![](images/colab.png)](https://colab.research.google.com/github/sfoucher/TraitementImagesPythonVol1/blob/main/notebooks/03-TransformationSpectrales.ipynb)

    <div style="border:0.5px solid silver;border-left:.3rem solid #00796d;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#e2efec;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADfUlEQVRYhb2XMXLbMBBFnzVKkSZ0ylRmJkVKMycwfQIrJzB9AVruMsNGLlCHwQVC3UC+AXUC02WKTOQ+hXGAjFNgIYIQZNkZxzvD4UhY7H7s/l0s9+7v73msJFWZAzmQAfvBcidPa5RePdbm3i4ASVWmwBQogOSRdpdAY5RuIvb2gX0H8kEASVXOxHkCGGAhT2uUvgt0M2x0CuBQ/r4BCqN05+m0wMQo3QKMtzjOgEYMGeAsdhpfxEkH1BK1GjhBUuU5H0RxIwKB4pWcYHDax0pSlalRehVxfiFghwACxQujdP0vjgMQ0ZOLfBt7ivvYsCc8EHLRy7GV4OQOy4su0C2wqYg5PzNKNz4HZticz7ewNxWd0xgw0bkFZt7+mHODTesCYCQbM+AcuMWyPjQ8websVHQugWPvOQPmwAE9CQFWEee5cw7CgaQqF1jGHrvy8JwXwHf5+SAvPMd32HI98pZvsOW3SqqyBmqj9Gokm06A24jzFBtGA3zaRUqvA7bifAm8xUYpF+c5NtozsH0gl00x4w09KdcEEyIW9O24M0ovAsbPjdKFB8iBbJOqNMDEAZjI2jov4iRzp/BJuY3ZSVX+AN4Bb5BUiY3CKB3yagGcJlWZjYAUMJELxAFbR0ZSsuYDfXh/Ah+B19ho1d7eczallXc2wpZeF1HKA2WQvAFTo3QtHbIAPgB/gFeB/p0AzxnKSt7pKOJ4IEEbTrHRasRwgy3NG+CLp+MkdrCB7ASwQ3Is03Pgd2R95x2yE4Aw3skKSKQxYZROjdK5RGnq6TgJh5YNGWPDl0XWWmwVTLDlCH0rbmRWWIiTGsulq4DMDmgb2E4d2JF3qjRQcmVZuD/E+Jn8/Ar8Aq7pm85aV4h3iL3SQ8nl3Y08RxNfQxrPEjiS2nf/N3KCC+ydcAl89lLhpA7eIQBjlO7G9GUzjSgX9FNO57qhOHroTmjoU9IGaxPspTUHGElY58BBWK+y5mbC66QqN27KwHiaVKW7NW/wUuKJs1FDfxtm2FzeAllk4HRETESnYdhwUmxY3awQHeW8m3VplM7XAGTRtU3/Ehmcjh0DiYDzB5JwfyeHeL8xlku9t9jcPctIFuxxtgczxUsMpb7zjej+77E8x5Z5OB9sByAbU9noPkymuz5MIvvdhwnApVF6FtN90U+zJwPwTvNsH6dPBhCAyXnmz/O/0JrtInNZu4wAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>Objectifs d’apprentissage visés dans ce chapitre</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">

    </div>
    </div>

    ### Librairies

    Les librairies qui vont être explorées dans ce chapitre sont les suivantes:

    -   [SciPy](https://scipy.org/)

    -   [NumPy](https://numpy.org/)

    -   [spyindex](https://github.com/awesome-spectral-indices/spyndex)

    -   [Rasterio](https://rasterio.readthedocs.io/en/stable/)

    -   [Xarray](https://docs.xarray.dev/en/stable/)

    -   [rioxarray](https://corteva.github.io/rioxarray/stable/index.html)

    Dans l'environnement Google Colab, seul `rioxarray` doit être installés
    """)
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %%capture
    # !pip install -qU matplotlib rioxarray xrscipy scikit-image pyarrow spyndex
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
    import rioxarray as rxr
    from scipy import signal
    import xarray as xr
    import xrscipy
    import spyndex
    import rasterio as rio

    return np, rxr, spyndex


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
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1a6O3L_abOfU7h94K22At8qtBuLMGErwo', output= 'sentinel2.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1_zwCLN-x7XJcNHJCH6Z8upEdUXtVtvs1', output= 'berkeley.jpg')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1dM6IVqjba6GHwTLmI7CpX8GP2z5txUq6', output= 'SAR.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1aAq7crc_LoaLC3kG3HkQ6Fv5JfG0mswg', output= 'carte.tif')
    # gdown.download('https://drive.google.com/uc?export=download&confirm=pbef&id=1iCZNYTv0qEZRzPhe22nPdpV4Ks7NsY3b', output= 'ASCIIdata_splib07b_rsSentinel2.zip')
    # !unzip -q ASCIIdata_splib07b_rsSentinel2.zip
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
    with rxr.open_rasterio('sentinel2.tif', mask_and_scale= True) as img_s2:
        print(img_s2)
    with rxr.open_rasterio('carte.tif', mask_and_scale= True) as img_carte:
        print(img_carte)
    return img_carte, img_s2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Qu'est ce que l'information spectrale?

    L'information spectrale touche à l'exploitation de la dimension spectrale des images (c.à.d le long des bandes spectrales de l'image). La taille de cette dimension spectrale dépend du type de capteurs considéré. Un capteur à très haute résolution spectrale par exemple aura très peu de bandes (4 ou 5). Un capteur multispectral pourra contenir une quinzaine de bande. À l'autre extrême, on trouvera les capteurs hyperspectraux qui peuvent contenir des centaines de bandes spectrales.

    ![Positions des bandes spectrales pour quelques capteurs ([source](https://landsat.gsfc.nasa.gov/article/sentinel-2a-launches-our-compliments-our-complements/))](images/Landsat.v.Sentinel-2-1.png){fig-align="center" width="6in"}

    Pour une surface donnée, la forme des valeurs le long de l'axe spectrale caractérise le type de matériau observé ainsi que son état. On parle souvent alors de signature spectrale. On peut voir celle-ci comme une généralisation de la couleur d'un matériau au delà des bandes visibles du spectre. L'exploitation de ces signatures spectrales est probablement un des principes les plus importants en télédétection qui le distingue de la vison par ordinateur. L'[USGS](https://www.sciencebase.gov/catalog/item/586e8c88e4b0f5ce109fccae) maintient une base de données spectrales acquises en laboratoire [@Kokaly-2017]. On peut observer sur la figure ci-dessous comment la forme et l'amplitude de trois signatures différentes peut changer en fonction du type de surface.
    """)
    return


app._unparsable_cell(
    r"""
    HOME= !pwd
    with open(f'{HOME[0]}/ASCIIdata_splib07b_rsSentinel2/S07SNTL2_Wavelengths_Sentinel2_(13_bands)_microns.txt','r') as f:
        # Read all lines, skipping the first line
        lines = f.read().split('\n')[1:]  
        # Filter out empty or whitespace-only lines before converting to float
        band_pos = [float(s.replace(' ', ''))*1000 for s in lines if s.strip()]

    with open('ASCIIdata_splib07b_rsSentinel2/ChapterV_Vegetation/S07SNTL2_Rangeland_C03-004_S08%_G27%_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        LawnGrass = [float(s.replace(' ', '')) for s in lines if s.strip()]

    with open('ASCIIdata_splib07b_rsSentinel2/ChapterL_Liquids/S07SNTL2_Water+Montmor_SWy-2+0.50g-l_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        Water = [float(s.replace(' ', '')) for s in lines if s.strip()]


    with open('ASCIIdata_splib07b_rsSentinel2/ChapterA_ArtificialMaterials/S07SNTL2_Concrete_GDS375_Lt_Gry_Road_ASDFRa_AREF.txt','r') as f:
        lines = f.read().split('\n')[1:]  
        Concrete = [float(s.replace(' ', '')) for s in lines if s.strip()]
    fig, ax= plt.subplots(figsize = (8,5))
    plt.plot(band_pos,LawnGrass, 'g.-')
    plt.plot(band_pos,Water, 'b.-')
    plt.plot(band_pos,Concrete, 'y.-')
    plt.legend(['Prairie','Eau','Béton'])
    ax.grid('on')
    ax.set_xlabel('Longueur d\'onde (nm)')
    ax.set_ylabel('Réflectance')
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Indices spectraux

    Il existe une vaste littérature sur les indices spectraux, le choix d'un indice plutôt qu'un autre dépend fortement de l'application visée, nous allons simplement couvrir les principes de base ici. Le principe d'un indice spectral consiste à mettre en valeur certaines caractéristiques saillantes du spectre comme des pentes, des gradients, etc.

    La librairie Python [Awesome Spectral Indices](https://awesome-ee-spectral-indices.readthedocs.io/en/latest/) maintient une liste de plus de 200 indices spectraux (radar et optiques). La liste complète est affichable avec la commande suivante:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.indices
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le détail d'un indice particulier, par exemple le \`NDVI\`, est aussi affichable:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.indices["NDVI"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `spyndex` pré-suppose une nomenclature prédéfinie des [bandes](https://awesome-ee-spectral-indices.readthedocs.io/en/latest/#expressions), on peut voir la correspondance sur le tableau ci-dessous:
    """)
    return


@app.cell
def _(spyndex):
    spyndex.bands
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Index | Noms | Spyndex | Noms                      |
    |-------|------|---------|---------------------------|
    | 1     | B01  | A       | Aérosol                   |
    | 2     | B02  | B       | Bleu                      |
    | 3     | B03  | G       | Vert                      |
    | 4     | B04  | R       | Rouge                     |
    | 5     | B05  | RE1     | Red edge 1                |
    | 6     | B06  | RE1     | Red edge 2                |
    | 7     | B07  | RE2     | Red edge 3                |
    | 8     | B08  | N       | Proche-infrarouge 1       |
    | 9     | B08A | N2      | Proche-infrarouge 2       |
    | 10    | B09  | \-      | Vapeur d'eau              |
    | 11    | B11  | S1      | Infra-rouge onde courte 1 |
    | 12    | B12  | S2      | Infra-rouge onde courte 1 |

    : Noms des bandes Sentinel-2

    Deux options sont possibles, on peut soit renommer les noms des bandes avec `xarray` ou "mapper" les noms vers les noms appropriés. Regardons les dimensions de notre jeux de données:
    """)
    return


@app.cell
def _(img_s2):
    img_s2.dims
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut simplement changer les index (`coords`) de la dimension `band`:
    """)
    return


@app.cell
def _(img_s2):
    sentinel2_bands = ['A', 'B', 'G', 'R', 'RE1', 'RE2', 'RE3', 'N', 'N2', 'WV', 'S1', 'S2']
    img_s2_1 = img_s2.sel(band=list(range(1, 13))).assign_coords({'band': sentinel2_bands})
    img_s2_1 = img_s2_1 / 10000  # normalisation en réflectance
    return img_s2_1, sentinel2_bands


@app.cell
def _(img_s2_1, plt, spyndex):
    from rasterio import plot
    idx = spyndex.computeIndex(index=['NDVI', 'GNDVI', 'SAVI'], params={'N': img_s2_1.sel(band='N'), 'R': img_s2_1.sel(band='R'), 'G': img_s2_1.sel(band='G'), 'L': 0.5})
    (fig, ax) = plt.subplots(2, 2, figsize=(9, 9))
    [a.axis('off') for a in ax.flatten()]
    plot.show(img_s2_1.sel(band=['R', 'G', 'B']).data / 0.3, ax=ax[0, 0], title='RGB')
    plot.show(idx.sel(index='NDVI'), ax=ax[0, 1], title='NDVI')
    plot.show(idx.sel(index='GNDVI'), ax=ax[1, 0], title='GNDVI')
    # Plot the indices (and the RGB image for comparison)
    plot.show(idx.sel(index='SAVI'), ax=ax[1, 1], title='SAVI')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On peut vérifier l'utilité des indices en vérifiant leur séparabilité pour certaines classes d'intérêts. Nous reprenons ici l'exemple de la section [@sec-05.02.02] pour vérifier l'utilité des indices `NDVI`, `NDWI` et `NDBI`:
    """)
    return


@app.cell
def _(img_carte, np, sentinel2_bands):
    from matplotlib.colors import ListedColormap
    import rasterio
    import geopandas
    from shapely.geometry import Point
    import pandas as pd
    couleurs_classes = {'NoData': 'black', 'Commercial': 'yellow', 'Nuages': 'lightgrey', 'Foret': 'darkgreen', 'Faible_végétation': 'green', 'Sol_nu': 'saddlebrown', 'Roche': 'dimgray', 'Route': 'red', 'Urbain': 'orange', 'Eau': 'blue', 'Tourbe': 'salmon', 'Végétation éparse': 'darkgoldenrod', 'Roche avec végétation': 'darkseagreen'}
    nom_classes = [*couleurs_classes.keys()]
    couleurs_classes = [*couleurs_classes.values()]
    cmap_classes = ListedColormap(couleurs_classes)
    img_carte_1 = img_carte.squeeze()
    class_counts = np.unique(img_carte_1.data, return_counts=True)
    sampled_points = []
    class_labels = []
    for class_label in range(1, 13):
        class_pixels = np.argwhere(img_carte_1.data == class_label)
        n_samples = min(100, len(class_pixels))
    # Liste vide des points échantillonnées
        np.random.seed(0)
        sampled_indices = np.random.choice(len(class_pixels), n_samples, replace=False)  # contient les étiquettes des classes
        sampled_pixels = class_pixels[sampled_indices]  # pour chacune des 12 classes
        sampled_points.extend(sampled_pixels)  # On cherche tous les pixels pour cette étiquette
        class_labels.extend(np.array([class_label] * n_samples)[:, np.newaxis])
    sampled_points = np.array(sampled_points)
    class_labels = np.array(class_labels)  # On se limite à 100 pixels par classe
    transformer = rasterio.transform.AffineTransformer(img_carte_1.rio.transform())
    transform_sampled_points = transformer.xy(sampled_points[:, 0], sampled_points[:, 1])
    points = [Point(xy) for xy in zip(transform_sampled_points[0], transform_sampled_points[1])]  # On les choisit les positions aléatoirement
    gdf = geopandas.GeoDataFrame(range(1, len(points) + 1), geometry=points, crs=img_carte_1.rio.crs)  # ceci permet de répliquer le tirage aléatoire
    coord_list = [(x, y) for (x, y) in zip(gdf['geometry'].x, gdf['geometry'].y)]
    with rasterio.open('sentinel2.tif') as src:
        values = [x[0:13] / 10000.0 for x in src.sample(coord_list)]  # On prends les positions en lignes, colonnes
    for (b, band) in enumerate(sentinel2_bands):
        gdf[band] = [x[b] for x in values]
    # Conversion en NumPy array
    # On peut naviguer les points à l'aide de la géoréférence
    gdf['class'] = class_labels  # On ajoute les points à la liste
    return couleurs_classes, gdf, nom_classes, pd


@app.cell
def _(couleurs_classes, gdf, nom_classes, pd, plt, spyndex):
    import seaborn as sns
    class_selected = [1, 3, 9]
    df = pd.concat([gdf[gdf['class'] == c] for c in class_selected], ignore_index=True)
    # On sélectionne trois classes
    idx_1 = spyndex.computeIndex(index=['NDVI', 'NDWI', 'NDBI'], params={'N': df['N'], 'R': df['R'], 'G': df['G'], 'S1': df['S1']})
    idx_1['Land Cover'] = [nom_classes[l] for l in df['class'].tolist()]
    colors = [couleurs_classes[c] for c in class_selected]
    # Compute the desired spectral indices
    plt.figure(figsize=(15, 15))
    g = sns.PairGrid(idx_1, hue='Land Cover', palette=sns.color_palette(colors))
    g.map_lower(sns.scatterplot)
    g.map_upper(sns.kdeplot, fill=True, alpha=0.5)
    g.map_diag(sns.kdeplot, fill=True)
    g.add_legend()
    # Plot a pairplot to check the indices behaviour
    plt.show()  # Add Land Cover to DataFrame
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![Visualisation des points d'une image Sentinel-2 pour trois classes](images/fig-classes-indices.png){fig-align="center"}

    ## Quiz

    ::: {.content-visible when-profile="production"}

    Utilisez la version html.
    :::
    """)
    return


@app.cell
def _():
    from code_complementaire.quizz_functions import Quiz, render_quizz
    Chap03Quiz = Quiz("quiz/Chap03.yml", "Chap03")
    render_quizz(Chap03Quiz)
    #import os
    #output_format = os.environ.get("QUARTO_PROFILE")
    #print(output_format)
    return


if __name__ == "__main__":
    app.run()
