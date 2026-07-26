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

    Dans l'environnement Google Colab, seul `rioxarray` doit être installé.
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
    | 6     | B06  | RE2     | Red edge 2                |
    | 7     | B07  | RE3     | Red edge 3                |
    | 8     | B08  | N       | Proche-infrarouge 1       |
    | 9     | B08A | N2      | Proche-infrarouge 2       |
    | 10    | B09  | WV      | Vapeur d'eau              |
    | 11    | B11  | S1      | Infra-rouge onde courte 1 |
    | 12    | B12  | S2      | Infra-rouge onde courte 2 |

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Le **NDVI** (*Normalized Difference Vegetation Index*) est l'indice le plus connu. Il se calcule à partir des bandes rouge ($R$) et proche-infrarouge ($N$) :

    $$ NDVI = \frac{N - R}{N + R} $$ {#eq-ndvi}

    La végétation en bonne santé réfléchit fortement le proche-infrarouge et absorbe le rouge : son NDVI est donc élevé (proche de $1$), alors que l'eau, le sol nu ou le bâti donnent des valeurs faibles, voire négatives. Le `GNDVI` remplace le rouge par le vert, le `SAVI` ajoute un facteur de correction du sol ($L$) et l'`EVI` (*Enhanced Vegetation Index*) corrige en plus l'effet de l'atmosphère à l'aide de la bande bleue ($B$), ce qui limite la saturation du NDVI sur la végétation dense [@Jensen2016]. On calcule ces quatre indices ci-dessous avec `spyndex.computeIndex` :
    """)
    return


@app.cell
def _(img_s2_1, plt, spyndex):
    from rasterio import plot
    idx = spyndex.computeIndex(index=['NDVI', 'GNDVI', 'SAVI', 'EVI'], params={'N': img_s2_1.sel(band='N'), 'R': img_s2_1.sel(band='R'), 'G': img_s2_1.sel(band='G'), 'B': img_s2_1.sel(band='B'), 'L': 0.5, 'g': 2.5, 'C1': 6.0, 'C2': 7.5})
    (fig, ax) = plt.subplots(2, 3, figsize=(13, 9))
    [a.axis('off') for a in ax.flatten()]
    plot.show(img_s2_1.sel(band=['R', 'G', 'B']).data / 0.3, ax=ax[0, 0], title='RGB')
    plot.show(idx.sel(index='NDVI'), ax=ax[0, 1], title='NDVI')
    plot.show(idx.sel(index='GNDVI'), ax=ax[0, 2], title='GNDVI')
    plot.show(idx.sel(index='SAVI'), ax=ax[1, 0], title='SAVI')
    plot.show(idx.sel(index='EVI'), ax=ax[1, 1], title='EVI')
    # Plot the indices (et l'image RGB pour comparaison)
    plt.tight_layout()  # constantes de l'EVI (gain + coefficients atmosphériques)
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

    ## Réduction de dimension

    La réduction de dimension vise à ne retenir que l'information principale d'un jeu de données. L'objectif est parfois d'éliminer le bruit d'un capteur ou de faciliter la visualisation en ne retenant que 3 bandes principales. Le degré d'information est souvent mesuré par la variance d'une bande, c'est-à-dire son contraste. L'analyse en composantes principales vise alors à ranger l'information contenue dans une image en ordre de variance décroissante.

    ### Transformations linéaires et produit matriciel

    Une **transformation linéaire de bandes** consiste à produire de nouvelles bandes par sommes pondérées des bandes d'origine. Chaque pixel étant un vecteur de valeurs (une par bande), appliquer les mêmes poids à tous les pixels revient à un simple **produit matriciel** (opérateur `@` dans NumPy). Sur un petit exemple, une matrice `M` transforme 2 bandes en 2 nouvelles combinaisons :
    """)
    return


@app.cell
def _(np):
    pixels = np.array([[10.0, 40.0], [20.0, 10.0], [5.0, 25.0]])
    M = np.array([[0.5, 0.5], [1.0, -1.0]])
    # 3 pixels (en lignes), 2 bandes (en colonnes)
    # Deux combinaisons de bandes définies par une matrice (2 sorties x 2 bandes)
    print(pixels @ M.T)  # moyenne des deux bandes  # différence des deux bandes  # produit matriciel : (3 pixels x 2 sorties)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'analyse en composantes principales pousse cette idée plus loin : au lieu de choisir les poids à la main, elle les **apprend des données** pour maximiser la variance retenue.

    ### Transformation Tasseled Cap (Kauth-Thomas)

    Un exemple historique et toujours largement utilisé de transformation linéaire à coefficients **fixes** (plutôt qu'appris comme en ACP) est la transformation *Tasseled Cap* (ou de Kauth-Thomas), qui combine les bandes réflectives en trois composantes interprétables physiquement : la **brillance** (*brightness*, liée au sol), la **verdure** (*greenness*, liée à la végétation) et l'**humidité** (*wetness*, liée à l'eau du sol et de la végétation) [@Jensen2016; @richards2022remote; @Schowengerdt2007]. Les coefficients ci-dessous, établis par Crist (1985) pour les bandes réflectives de Landsat TM, sont appliqués ici, à titre d'illustration, aux bandes analogues de Sentinel-2 (`B`, `G`, `R`, `N`, `S1`, `S2`) ; chaque capteur possède en pratique ses propres coefficients publiés.
    """)
    return


@app.cell
def _(img_s2_1, np, plt):
    # Coefficients de Crist (1985) pour les bandes réflectives Landsat TM (B, G, R, N, S1, S2),
    # appliqués ici à titre d'illustration aux bandes analogues de Sentinel-2
    tc_coeffs = np.array([[0.3037, 0.2793, 0.4743, 0.5585, 0.5082, 0.1863], [-0.2848, -0.2435, -0.5436, 0.7243, 0.084, -0.18], [0.1509, 0.1973, 0.3279, 0.3406, -0.7112, -0.4572]])
    tc_bands = ['B', 'G', 'R', 'N', 'S1', 'S2']  # Brightness
    X_tc = img_s2_1.sel(band=tc_bands).data.reshape(len(tc_bands), -1)  # Greenness
    (brightness, greenness, wetness) = (tc_coeffs @ X_tc).reshape(3, *img_s2_1.shape[1:])  # Wetness
    (fig_1, ax_1) = plt.subplots(ncols=3, figsize=(10, 4))
    for (a, im, title) in zip(ax_1, (brightness, greenness, wetness), ('Brightness', 'Greenness', 'Wetness')):
        a.imshow(im)
        a.set_title(title)  # (6, pixels)
        a.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Contrairement à l'ACP, ces coefficients ne dépendent pas de l'image : ils permettent donc de comparer directement les composantes entre plusieurs scènes, ce que l'ACP (dont les axes sont recalculés à chaque image) ne permet pas.

    ### Analyse en composantes principales (ACP)

    L'analyse en composantes principales (ACP) est probablement la plus employée. En théorie, l'ACP n'est valide que sur des données gaussiennes, c'est-à-dire que le nuage de points des données a la forme d'une ellipse à $N$ dimensions. Cette ellipse est caractérisée par des directions principales (grand axe versus petit axe). La première composante est celle du grand axe de l'ellipse, pour laquelle la donnée présente le maximum de variation. L'ACP est une décomposition **linéaire** : les composantes principales sont des sommes pondérées des valeurs originales.

    Concrètement, on aplatit le cube en une table `pixels × bandes`, on **centre** les données, puis on diagonalise la **matrice de covariance** (`np.linalg.eigh`, adaptée aux matrices symétriques). Les vecteurs propres donnent les directions principales, et les valeurs propres la variance portée par chacune :
    """)
    return


@app.cell
def _(img_s2_1, np):
    # On aplatit le cube (bandes x pixels) en une table (pixels x bandes)
    cube = img_s2_1.to_numpy()  # (12, lignes, colonnes), réflectance
    (B, H, W) = cube.shape
    X = cube.reshape(B, H * W).T  # (pixels, bandes)
    X_c = X - X.mean(axis=0)  # centrage : moyenne nulle par bande
    cov = np.cov(X_c, rowvar=False)
    # Matrice de covariance (12 x 12), puis vecteurs et valeurs propres
    (valeurs, vecteurs) = np.linalg.eigh(cov)
    ordre = np.argsort(valeurs)[::-1]  # eigh : matrice symétrique
    (valeurs, vecteurs) = (valeurs[ordre], vecteurs[:, ordre])  # variance décroissante
    ratio = valeurs / valeurs.sum()
    print('Variance expliquée (5 premières) :', ratio[:5].round(3))
    print('Cumul des 3 premières composantes :', round(ratio[:3].sum(), 3))
    return B, H, W, X, X_c, ratio, vecteurs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La projection des pixels sur les vecteurs propres est, elle aussi, un **produit matriciel**. On récupère ensuite un cube de composantes rangées par variance décroissante :
    """)
    return


@app.cell
def _(B, H, W, X_c, vecteurs):
    # Projection des pixels sur les directions principales
    composantes = (X_c @ vecteurs).T.reshape(B, H, W)   # (composantes, lignes, colonnes)
    print("Cube des composantes :", composantes.shape)
    return (composantes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Les trois premières composantes concentrent l'essentiel de l'information (ici plus de 98 % de la variance). On les visualise sous forme d'un composé coloré, à côté de l'éboulis (*scree plot*) des variances :
    """)
    return


@app.cell
def _(B, composantes, np, plt, ratio):
    (fig_2, ax_2) = plt.subplots(1, 2, figsize=(10, 4))
    ax_2[0].bar(range(1, B + 1), ratio)
    ax_2[0].set_xlabel('Composante')
    ax_2[0].set_ylabel('Variance expliquée')
    ax_2[0].set_title('Éboulis (scree plot)')
    # Composé coloré des 3 premières composantes (étirement min-max par composante)

    def etirer(x):
        return (x - x.min()) / (x.max() - x.min())
    rgb = np.dstack([etirer(composantes[i]) for i in range(3)])
    ax_2[1].imshow(rgb)
    ax_2[1].set_title('Composantes 1-2-3 (RGB)')
    ax_2[1].axis('off')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    La première composante ressemble souvent à une image de brillance globale, tandis que les suivantes isolent des contrastes plus fins (végétation, eau). La même décomposition s'obtient de façon numériquement plus stable par **décomposition en valeurs singulières** (`np.linalg.svd`) appliquée aux données centrées. La réduction de dimension prépare aussi la classification (@sec-chap05) en concentrant l'information utile dans quelques bandes.

    ### Reconstruction et erreur de compression

    Conserver seulement les $k$ premières composantes revient à **compresser** l'image : la reconstruction s'obtient en projetant sur les $k$ premiers vecteurs propres, puis en revenant dans l'espace original (l'opération inverse du produit matriciel de projection). On peut alors mesurer l'erreur de reconstruction (RMSE) en fonction de $k$ [@richards2022remote] :
    """)
    return


@app.cell
def _(B, X, composantes, np, plt, vecteurs):
    def erreur_reconstruction(k):
        proj_k = composantes[:k].reshape(k, -1).T  # (pixels, k)
        X_approx = proj_k @ vecteurs[:, :k].T + X.mean(axis=0)  # (pixels, bandes)
        return np.sqrt(np.mean((X - X_approx) ** 2))  # RMSE
    erreurs = [erreur_reconstruction(k) for k in range(1, B + 1)]
    (fig_3, ax_3) = plt.subplots(figsize=(5, 4))
    ax_3.plot(range(1, B + 1), erreurs, 'o-')
    ax_3.set_xlabel('Nombre de composantes conservées (k)')
    ax_3.set_ylabel('Erreur de reconstruction (RMSE)')
    ax_3.grid(True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    L'erreur diminue rapidement avec le nombre de composantes conservées, ce qui confirme que l'essentiel de l'information est capté par les toutes premières composantes — ici, une poignée de composantes suffit à approcher fidèlement les 12 bandes d'origine.

    L'ACP suppose une distribution gaussienne des données et ne retient que des combinaisons linéaires classées par variance décroissante, ce qui n'est pas toujours le critère le plus pertinent. La transformation en **fraction de bruit minimum/maximum** (*Minimum/Maximum Noise Fraction*, MNF) classe plutôt les composantes par rapport signal-sur-bruit décroissant, ce qui la rend préférable pour les images hyperspectrales bruitées [@richards2022remote]. L'**analyse en composantes indépendantes** (ICA) relâche quant à elle l'hypothèse gaussienne en recherchant des composantes statistiquement indépendantes plutôt que simplement décorrélées.

    ## Points clés

    <div style="border:0.5px solid silver;border-left:.3rem solid #357cc0;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#eef5fb;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IB2cksfwAAA/pJREFUWIXNl01sVFUYhp/vzLSlDTbiTCmpoEQT5SemQQNaFw12ftCQrtSmKxLiAmUp0UTsz51prcYFKxM10ZCwarCuiAlMWyQuICkQ7KKlmmBiqDWlc52m1jKkvedz0TuVInTujNH6rr6595z3ec89d+45RwioV/p+rVv0wruNyi4LuwV2Abv922MK4wbGrOi48bzxjLPlVhBfKdagpTf3eEi9bpTDQcP6zic9CaXOd2z6uawATSduVm/8fcN7CO+CVAFLwA8CowqjqjKq4aXvvUWRsIQaRbRRoFGhEXgaCIPeQfl4/qH8h5fe3nY7cICkk92hhgH/EVuB/iXxus531t8IMviWnuknwxpKK7QDBhgTy2sZJzpRNEA8fWuPYIaBTcB1i7wx3BW5FAR8r2Jpt8mgXwI7gZxiY0Ndm689MEDCmWnAyAjwKMg3G+ydtjNOw0I58IJanamavKk6DXoQ+AWr+waduqm/BXj9tIZmr/92HtFmhW9z9ZEDV4/I4j+BF/Tc51qxado9J/ASKt89vPORlq/axMOfHwBmJ9xjiDYDk0u2sq0YPJlyE4l0diSRzo4kU25irbZXj8jikq1sAyYRbZ6dcI8V7hmAZK+7DegGVIXDF5zabNFhiX4K7AX2+vWauuDUZlU4DCjQ7TOXA1hLB1CDSP9QZ3SoKLxMDXVGhxDpB2p8JibWNxcR9BBgrWedwG4qbwGXgct+HUg+wwp6KNY3F5FEauYIIp8B5wa7oi+XObiSlEhnzwIHUH3TIJIEUNWv/wv4KpZIMgy6B4SQmItBDeK97gvi2UYR2a7IdhHNZTqjR4P2D4m5aFFA94RBtgLMbVz4KaiBWJKIHFWoB0WVT4L2LbA2zlcDstUAFYA+aLG4nwa7ImlFPlq5oIyUEsBnKVBhArS/r0TYUahDRksKcLcMsAhI04mb1SX1VN3nV7mzHdEfS+nqswRYNKCTALXzNU8ENWh1pmqAZ/yflxHRUgL8xdJJA3INwFP7YlCD2+ENzy5vOEApbf5Xs+SaQTUDICKvBjUQ6xUeP0ZLn/8VlmrG2IqqASAPJGLOzFNBDFRYCeCFbUkBfEYCyNuKqgEzfLzWVeQUYEzIBFoLROV5lt+iG8Pv10+XEsBnGEVODR+vdQ2AMfQCC6i2x3uy8QA+m1me/4ZE2u1KpmYCBY/3ZOOotgMLPnN5Oc50RG4CKUBEObnfmYuuZaSiZ/xSQOtCar4oBt/vzEVFOen//VI+s8wtmaq0fDD7WLjqTjbzzpY/isHX2pKt+6Z01ad40KmbUmwrkAM9mDeVV2Jpt6lceCztNuVN5RUfnlNs691w/pcHk4LW9Wi2ajTrdTi9V//W8fxPxif/DjJKAKcAAAAASUVORK5CYII=" width="16" height="16" alt="\"/><span><strong>À retenir</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ul>
    <li>L’<strong>information spectrale</strong> exploite la dimension des bandes ; la <strong>signature spectrale</strong> caractérise le type et l’état d’un matériau — une généralisation de la couleur au-delà du visible.</li>
    <li>Le nombre de bandes distingue les capteurs : <strong>multispectral</strong> (une quinzaine) vs <strong>hyperspectral</strong> (des centaines).</li>
    <li>Un <strong>indice spectral</strong> met en valeur des caractéristiques du spectre (pentes, gradients) et améliore la <strong>séparabilité</strong> des classes d’intérêt.</li>
    <li>La librairie <strong><code>spyndex</code></strong> (Awesome Spectral Indices) donne accès à plus de 200 indices ; elle suppose une <strong>nomenclature de bandes</strong> (<code>N</code>, <code>R</code>, <code>G</code>, <code>S1</code>…).</li>
    <li><code>spyndex.computeIndex</code> applique un indice à partir des bandes nommées ; renommer les bandes (<code>assign_coords</code>) facilite l’usage.</li>
    <li>Le <strong>NDVI</strong> <span class="math inline">\(= (N - R)/(N + R)\)</span> est élevé pour la végétation dense.</li>
    <li>Une <strong>transformation linéaire de bandes</strong> est un <strong>produit matriciel</strong> (<code>@</code>) ; l’<strong>ACP</strong> apprend les poids optimaux (covariance + vecteurs propres) pour ranger l’information par variance décroissante et <strong>réduire la dimension</strong>.</li>
    <li>La transformation <strong>Tasseled Cap</strong> (coefficients fixes, comparables entre scènes) et l’ACP (coefficients appris, propres à chaque image) illustrent deux façons de construire une transformation linéaire de bandes ; la <strong>reconstruction tronquée</strong> quantifie la perte d’information selon le nombre de composantes conservées.</li>
    </ul>
    </div>
    </div>

    ## Exercices

    <div style="border:0.5px solid silver;border-left:.3rem solid #e34692;border-radius:.25rem;background:#FAF9FF;margin:1em 0;">
    <div style="display:flex;align-items:center;gap:.5rem;padding:.4em .6em;background:#fbe8f2;font-weight:700;"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAADP0lEQVRYha2XT3LaMBjFf3SyD91rBnqC0BOUbuJl6AkwB9CUnKD0BCXxAeKcIGSpVZ0bwAkKEx8ATkAXemoUgm0I/WY8smVJ7/n78yS3ttstp1iZZF0g1WNhnC3Un6o/N87mVfNbpxAQ+Bw4j7p/qv0R9Y2qSHx4N7q3scBvBLwS8A/dj4ANcCePvLFTPVAAX4yzraivDxCFogcUIvrGE6cSSIE74KdxdlIzrpLEqSGY4V2d1g0yzs6BPnvCcRIB4+waWAKdMsna7yHR2m63aPL4COzCOFuUSZYDQ+DeOJseMjEKB8bZduv58ratjosjCMSltgJ68gZlkg20+KyGRIrPndEZMBD4AuiHhSom9oHfeszxXusAkzLJ1vhc6GjsChjI9bs2UFt8ALp6GDeAt4GpHtfG2SUvMf2O90YHrwk3us/3rJMDV8CTcXZ5VgUYTehroY66NmFh4+w8kuI2r6X4OzthLZNsjM+ZBfJCLQF99Qxfvwu87E5iT+l+ujMvuPgp6kuBX/qAf6Fu8kBP4I/G2UHD2NjGAhpH4He74IcQCNYtk6xdlSNBfoGlcuMLPsbzPeCvkrL1fHk7wSfQ1xC/ncXnvMRyhU/Wmd7tK+ERPjmHwL3aveBwmBL2tdACn4gPSjzwyXchgEf1TXVtmsAPImCcXRtnU+NsT0QCMPgcQQADkTjHV0QgXgkOr3MglUzmu7HWF8dJ2I1keBMBFPgan4lk3vSBsQeG+DJZikgAT4E/ejeMxob7eA/J8aE6Bx7wqlm7x8QErqPJ8aSJ2nuNAV/f18DneG9XuHrAN172i+WhBMJ2CYqtsrwDLLTbBVevjbPTqtgaZ2d1B5QqAkHVFsCFYlxE5OL2qkyyWZlk46ZzwFEEZEHFhvgSW6kvEBwFEvi8KE4h8YaAxKgLfMWLU3dH+3PgIz7OG5FM30tgrxQLsKiapPcz7W53+Lr/fwSaTGU64KValjXDezXvjidQJtkUfwAJ9lj360WDd44iIEUM4Nf4A0ilzB5iZ0BIsJSauMu6am+Ms9O6gZGa1hJsPV/edvFSC14DKs+FeHeG0lzWc/13mPmkM8J+AvovGOC30E7VwHfYEw2/5gB/AcMlhsUeVwFpAAAAAElFTkSuQmCC" width="16" height="16" alt="\"/><span><strong>À vous de jouer</strong>
    </span></div>
    <div style="padding:.3em .6em;font-size:.95em;">
    <ol type="1">
    <li>Calculez le <strong>NDWI</strong> (eau) et le <strong>NDBI</strong> (bâti) avec <code>spyndex</code> sur <code>img_s2</code>, puis affichez-les côte à côte avec le NDVI.
    </li>
    <li>Comparez les <strong>signatures spectrales</strong> de deux surfaces supplémentaires de la base USGS (p. ex. neige, végétation sèche) sur les bandes Sentinel-2.
    </li>
    <li>Parcourez <code>spyndex.indices</code>, choisissez un indice adapté à l’eau ou aux sols, identifiez les bandes qu’il requiert, et calculez-le sur <code>img_s2</code>.
    </li>
    <li>Renommez les bandes de <code>img_s2</code> avec la nomenclature <code>spyndex</code> et vérifiez le résultat avec <code>img_s2.coords['band']</code>.
    </li>
    <li><em>(produit matriciel)</em> Construisez une matrice <code>2 × 4</code> transformant les 4 bandes de <code>RGBNIR_of_S2A.tif</code> en deux nouvelles bandes (brillance moyenne et différence PIR - Rouge) à l’aide de l’opérateur <code>@</code>, puis affichez-les.
    </li>
    <li><em>(ACP)</em> Réalisez l’ACP de <code>img_s2</code>, affichez la <strong>variance expliquée</strong> par chaque composante (éboulis), et vérifiez combien de composantes sont nécessaires pour atteindre 95 % de variance cumulée.
    </li>
    <li><em>(Tasseled Cap)</em> Appliquez la transformation Tasseled Cap à une autre combinaison de bandes (p. ex. en remplaçant <code>S1</code> par <code>RE1</code>) et comparez visuellement les composantes obtenues à celles de la section.
    </li>
    <li><em>(reconstruction)</em> À partir de l’ACP de <code>img_s2</code>, déterminez le nombre minimal de composantes nécessaires pour obtenir une erreur de reconstruction (RMSE) inférieure à 0.01.
    </li>
    </ol>
    </div>
    </div>

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
