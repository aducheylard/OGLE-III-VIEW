'''
CODIGO HECHO POR ANDRE DUCHEYLARD L.
GITHUB.COM/ADUCHEYLARD
'''

import matplotlib.pyplot as plt
import pandas as pd

def filtra_clase_df(df, clase):
    '''
    Los tipos de clase son ED, ESD, EC, cep, dsct, RRab, RRc, std, Mira, SRV, OSARG....
    '''
    df = df[(df['Class'] == clase)]
    return df

def grafica_OGLE_class(df_OGLE_dataset_class_list, n, titulo, eje_x, eje_y, forma, error):
    '''
    Grafica las light curve unfolded.
    Recibe una lista de df con este formato: [ID][CLASS][PATH][N]
    Donde,
    ID: Es el id de la medicion,
    CLASS: La clase de la estrella
    PATH: La ruta de donde estan almacenados los datos (si, estan en otro archivo...../LCs/archivo_con_datos.dat)
    N: La cantidad de mediciones que tiene el ID en particular...Si 'N' == 0, se imprimen TODAS las instancias de medicion

    Los parametros de la funcion son:
    df_OGLE_dataset_class_list: Una lista de dataframes filtrados previamente para tener datos de OGLE.
    n: Numero de instancias a graficar de cada clase
    titulo: Titulo del grafico
    eje_x: Nombre del eje x de cada subgrafico
    eje_y: Nombre del eje y de cada subgrafico
    forma: La forma con que se va a graficar...('o-', '-', etc...)
    erroor: Booleano para graficar con los errores correspondientes.
    '''
    fig, axs = plt.subplots(3, 3)  # CREAMOS UN SUBPLOT DE X, Y GRAFICOS
    fig.tight_layout()
    fig.suptitle(titulo, fontsize=26)
    fig.subplots_adjust(top=0.85)

    plots_dibujados = []  # Se almacenan ls subplot donde ya se dibujo
    for df_clase in df_OGLE_dataset_class_list:  # Recorremos la lista de DF's
        for ax in axs.flat:  # Recorremos los subplots para dibujar
            if ax in plots_dibujados:  # Verificamos que no se haya dibujado en el subplot
                #print("Ya dibuje en este plot")
                continue
            plots_dibujados.append(ax)  # Se agrega el subplot donde vamos a dibujar a la lista
            ite = 1  # Iniciamos un iterador para contar la cantidad de instancias a dibujar (Dibujar las 'N' instancias que se paso por parametro)
            for ruta in df_clase['Path']:  # Recorremos las rutas de las mediciones
                if ite <= n or n == 0:  # Verificamos cuantas mediciones se han graficado
                    df_light_curve = pd.read_csv(ruta, names=['Tiempo', 'Magnitud', 'Error'], sep=' ')  # Obtenemos el df de la medicion a graficar
                    ax.set_title(df_clase.iloc[0][1])  # Ponemos nombre de la clase a cada subplot desde la lista de DF's
                    ax.set(xlabel=eje_x, ylabel=eje_y)
                    if error:  # Se grafica segun se quiera considerar el error o no
                        ax.errorbar(df_light_curve['Tiempo'], df_light_curve['Magnitud'], yerr=df_light_curve['Error'], fmt=forma, ecolor='red')
                    else:
                        ax.plot(df_light_curve['Tiempo'], df_light_curve['Magnitud'], forma)
                else:
                    break
                ite += 1
            break
    plt.show()


nombreArchivo = "./OGLE_dataset_SAMPLE.dat"
df_ALL_dataset = pd.read_csv(nombreArchivo)
df_OGLE_dataset = df_ALL_dataset[(df_ALL_dataset['ID'].str.contains("OGLE"))] # FILTRAMOS EL DATASET DONDE EL ID CONTENGA 'OGLE', SOLAMENTE QUEREMOS GRAFICAR ESE


type_of_classes = df_ALL_dataset['Class'].unique()  # Obtenemos las clases que existen en el DF. ['ED' 'ESD' 'EC' 'cep' 'dsct' 'RRab' 'RRc' 'std' 'OSARG' 'SRV' 'Mira']
df_OGLE_dataset_class_list = []
for i in range(type_of_classes.__len__()):
    '''
    Filtramos y ordenamos el df por clase
    '''
    df_filtrado = filtra_clase_df(df_OGLE_dataset, type_of_classes[i])
    if not df_filtrado.empty:  # Aseguramos que el df filtrado no este vacio (Puede que para x clase no hayan datos de OGLE)
        df_OGLE_dataset_class_list.append(df_filtrado)


grafica_OGLE_class(df_OGLE_dataset_class_list, 3, "Unfolded Light Curve per Class", "Tiempo", "Magnitud", "-", False)