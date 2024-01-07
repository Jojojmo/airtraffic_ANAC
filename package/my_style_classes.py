import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from .supply_format import format_ticks



def fast_instance(data, x=None, y=None, title=None):
    """
    Função utilitária para criar um dicionário para ser utilizado em uma instância para configurações de gráfico.

    Parâmetros:
    - data (pd.DataFrame): Conjunto de dados para o gráfico.
    - x (str): Nome da coluna a ser usada no eixo x.
    - y (str): Nome da coluna a ser usada no eixo y.
    - title (str): Título do gráfico.

    Retorna:
    - dict: Dicionário contendo configurações para criar um gráfico com base nos parâmetros fornecidos.

    Exemplo de Uso:
    ```python
    # Criar uma instância rápida para um gráfico de dispersão
    scatterplot_instance = fast_instance(data=my_data, x='column_x', y='column_y', title='Meu Scatterplot')
    ```
    """
    chart_instance = {"grafico": {"data": data}}

    for arg_name in ["x", "y"]:
        arg_value = locals().get(arg_name)
        if arg_value is not None:
            chart_instance["grafico"][arg_name] = arg_value

    title_value = locals().get("title")
    if title_value is not None:
        chart_instance["titulo"] = {"label": title_value}

    return chart_instance


class My_styles:
    """
    Uma classe para gerenciar e personalizar estilos visuais para diferentes tipos de gráficos.

    Parâmetros:
    - type_style (str): O tipo de estilo de gráfico a ser personalizado (por exemplo, 'scatterplot', 'barplot').
    - **kwargs: Argumentos adicionais de palavra-chave para atualizar parâmetros de estilo específicos.

    Métodos:
    - __init__(type_style, **kwargs): Inicializa o objeto My_styles, lê os estilos padrão de um arquivo JSON e
      atualiza os estilos com base nos argumentos de palavra-chave fornecidos.
    - read_styles(): Lê os estilos padrão de um arquivo JSON e define os atributos correspondentes.
    - update_style_for_dict(**kwargs): Atualiza parâmetros de estilo específicos com base nos argumentos de palavra-chave.

    Atributos:
    - __type_style (str): O tipo de estilo de gráfico sendo personalizado.
    - Outros atributos: Definidos dinamicamente com base no conteúdo do arquivo JSON para o type_style especificado.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_styles para um scatterplot com um valor alpha personalizado
    estilo_scatterplot = My_styles('scatterplot', grafico={'alpha': 0.5})

    # Acessar atributos definidos dinamicamente com base no arquivo JSON
    label_titulo_scatterplot = estilo_scatterplot.titulo['label']
    ```
	"""
    def __init__(self, type_style, **kwargs):
        self.__type_style = type_style
        self.read_styles()        
        self.update_style_for_dict(**kwargs)

    def read_styles(self):
        """
        Lê os estilos padrão de um arquivo JSON e define os atributos correspondentes.
        Não há parâmetros de entrada.
        """
        script_dir = os.path.dirname(os.path.realpath(__file__))
        styles_path = os.path.join(script_dir, 'styles', 'my_styles.json')

        with open(styles_path, 'r', encoding='utf8') as estilos:
            estilo = json.load(estilos)

        for chave, valor in estilo[self.__type_style].items():
            setattr(self, chave, valor)

    def update_style_for_dict(self, **kwargs):
        """
        Atualiza parâmetros de estilo específicos com base nos argumentos de palavra-chave.
        
        Parâmetros:
        - **kwargs: Argumentos de palavra-chave contendo pares chave-valor para atualizar os estilos.
        """
        for chave, valor in kwargs.items():
            if chave in self.__dict__:
                getattr(self, chave).update(valor)


def pre_make(func):
    """
    Decorador que define configurações prévias para a criação de um gráfico.

    Configurações realizadas:
    - Configura o estilo do Seaborn com base em self.estilo, se existir.
    - Configura o tamanho da figura com base em self.tamanho.
    - Configura o título do gráfico com base em self.titulo.

    Parâmetros:
    - func (callable): Função que gera o conteúdo principal do gráfico.

    Exemplo de Uso:
    ```python
    @pre_make
    def make_scatterplot(self):
        # Conteúdo principal para criar um scatterplot
        # ...
    ```

    """
    def closure(self):
        sns.reset_defaults()
        sns.set(**self.estilo if hasattr(self, 'estilo') and self.estilo else {})

        plt.figure(**self.tamanho)
        plt.title(**self.titulo)
        
        func(self)
        sns.set_palette(self.estilo['palette'] if hasattr(self.estilo, 'palette') else {})
        plt.show()
    return closure


def decorator_filter_kw(my_list):
    """
    Decorador que filtra as configurações do gráfico com base em uma lista fornecida.

    Parâmetros:
    - my_list (list): Lista de chaves a serem mantidas nas configurações do gráfico.

    Retorna:
    - closure (callable): Função interna que filtra as configurações do gráfico com base em my_list.

    Exemplo de Uso:
    ```python
    @decorator_filter_kw(['x', 'y'])
    filter_kwargs(self):
        # Conteúdo principal para criar o gráfico com configurações filtradas
        # ...
    ```

    """
    def run_filter(func):
        def closure(self):
            filter_kwargs = dict()
            for key,value in self.grafico.items():
                if key not in my_list:
                    filter_kwargs[key] = value
            return filter_kwargs
        return closure
    return run_filter


class My_barplot(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para gráficos de barras.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs): Inicializa o objeto My_barplot com o tipo de estilo 'barplot' e parâmetros adicionais.

    - make():
      Método decorado com @pre_make que cria um gráfico de barras usando Seaborn.

    - ax_label_outbar(ax):
      Adiciona rótulos fora das barras no eixo x do gráfico de barras.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_barplot com estilos personalizados
    my_custom_barplot = My_barplot(titulo={'label': 'Meu Gráfico de Barras' ...})

    # Chamar o método make para gerar o gráfico
    my_custom_barplot.make()
    ```

    """
    def __init__(self, **kwargs):
        super().__init__(type_style="barplot", **kwargs)
    
    
    @pre_make
    def make(self):
        """
        Método decorado com @pre_make que cria um gráfico de barras usando Seaborn.

        Retorna:
        - None
        """
        ax = sns.barplot(**self.grafico)
        self.ax_label_outbar(ax)
        sns.despine()


    def ax_label_outbar(self,ax):
        """
        Adiciona rótulos fora das barras no eixo x do gráfico de barras.

        Parâmetros:
        - ax (matplotlib.axes.Axes): Eixo do gráfico de barras.

        Retorna:
        - None
        """
        if self.grafico["orient"] == 'h':
            x_max = self.grafico["data"][self.grafico["x"]].max()
            for i, v in enumerate(self.grafico["data"][self.grafico["x"]]):
                ax.text(v * 1.01, i, str(format_ticks(v, x_max)), color='black', va='center', fontweight='bold')
            ax.set(xticks=[])
        elif self.grafico["orient"] == 'v':
            y_max = self.grafico["data"][self.grafico["y"]].max()
            for i, v in enumerate(self.grafico["data"][self.grafico["y"]]):
                ax.text(i, v * 1.01, str(format_ticks(v, y_max)), color='black', ha='center', fontweight='bold')
            ax.set(yticks=[])



class My_scatterplot(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para gráficos de dispersão.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs): Inicializa o objeto My_scatterplot com o tipo de estilo 'scatterplot' e parâmetros adicionais.

    - make():
      Método decorado com @pre_make que cria um gráfico de dispersão usando Seaborn.

    - axis(scatter_plot):
      Configura os eixos do gráfico de dispersão.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_scatterplot com estilos personalizados
    my_custom_scatterplot = My_scatterplot(titulo={'label': 'Meu Gráfico de Dispersão' ...})

    # Chamar o método make para gerar o gráfico
    my_custom_scatterplot.make()
    ```

    """
    def __init__(self,**kwargs):
        super().__init__(type_style="scatterplot", **kwargs)

    
    @pre_make
    def make(self):
        """
        Método decorado com @pre_make que cria um gráfico de dispersão usando Seaborn.

        Retorna:
        - None
        """
        scatter_plot = sns.scatterplot(**self.grafico)
        scatter_plot.set(**self.eixos)
        self.axis(scatter_plot)

    
    def axis(self,scatter_plot):
        """
        Configura os eixos do gráfico de dispersão.

        Parâmetros:
        - scatter_plot (seaborn.axisgrid.FacetGrid): Objeto que representa o gráfico de dispersão.

        Retorna:
        - None
        """
        max_axis_x = self.grafico["data"][self.grafico["x"]].max()
        max_axis_y = self.grafico["data"][self.grafico["y"]].max()
        scatter_plot.xaxis.set_major_formatter(FuncFormatter(lambda x, p: format_ticks(x, max_axis_x, p)))
        scatter_plot.yaxis.set_major_formatter(FuncFormatter(lambda y, p: format_ticks(y, max_axis_y, p)))
        scatter_plot.tick_params(axis='y', labelsize=10)
        

class My_histplot(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para gráficos de histograma.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs): Inicializa o objeto My_histplot com o tipo de estilo 'histplot' e parâmetros adicionais.

    - make():
      Método decorado com @pre_make que cria um gráfico de histograma usando Seaborn.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_histplot com estilos personalizados
    my_custom_histplot = My_histplot(titulo={'label': 'Meu Gráfico de Histograma' ...})

    # Chamar o método make para gerar o gráfico
    my_custom_histplot.make()
    ```

    """
    def __init__(self, **kwargs):
        super().__init__(type_style="histplot", **kwargs)


    @pre_make
    def make(self):
        """
        Método decorado com @pre_make que cria um gráfico de histograma usando Seaborn.

        Retorna:
        - None
        """
        histogram_plot = sns.histplot(**self.grafico)
        histogram_plot.set( **self.eixos) 


class My_boxplot(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para gráficos de boxplot.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs):
      Inicializa o objeto My_boxplot com o tipo de estilo 'boxplot' e parâmetros adicionais.
      Atualiza o rótulo do título incluindo o número de outliers.

    - quantidade_outliers():
      Calcula o número de outliers com base nos quartis e no método IQR.

    - make():
      Método decorado com @pre_make que cria um gráfico de boxplot usando Seaborn.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_boxplot com estilos personalizados
    my_custom_boxplot = My_boxplot(titulo={'label': 'Meu Gráfico de Boxplot' ...})

    # Chamar o método make para gerar o gráfico
    my_custom_boxplot.make()
    ```

    """
    def __init__(self,**kwargs):
        super().__init__(type_style="boxplot",**kwargs)
        self.titulo["label"] = self.titulo['label'] + f"\nNúmero de Outliers:{self.quantidade_outliers()}"


    def quantidade_outliers(self):
        """
        Calcula o número de outliers com base nos quartis e no método IQR.

        Retorna:
        - int: Número de outliers no conjunto de dados.
        """
        Q1 = self.grafico["data"][self.grafico["y"]].quantile(0.25)
        Q3 = self.grafico["data"][self.grafico["y"]].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((self.grafico["data"][self.grafico["y"]] < lower_bound) |
                    (self.grafico["data"][self.grafico["y"]] > upper_bound))
        return sum(outliers)


    @pre_make
    def make(self):
        """
        Método decorado com @pre_make que cria um gráfico de boxplot usando Seaborn.

        Retorna:
        - None
        """
        sns.boxplot(**self.grafico)


class My_headmap(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para mapas de calor.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs):
      Inicializa o objeto My_heatmap com o tipo de estilo 'heatmap' e parâmetros adicionais.

    - make():
      Método decorado com @pre_make que cria um mapa de calor usando Seaborn.

    - filter_kwargs():
      Método decorado com @decorator_filter_kw para filtrar configurações específicas do gráfico.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_heatmap com estilos personalizados
    my_custom_heatmap = My_heatmap(titulo={'label': 'Meu Mapa de Calor' ...})

    # Chamar o método make para gerar o mapa de calor
    my_custom_heatmap.make()
    ```

    """
    def __init__(self,**kwargs):
        super().__init__(type_style='heatmap',**kwargs)

    @pre_make
    def make(self):
        """
        Método decorado com @pre_make que cria um mapa de calor usando Seaborn.

        Retorna:
        - None
        """
        correlation_matrix = round(self.grafico['data'].corr(),2)
        sns.heatmap(data=correlation_matrix,
                    xticklabels= self.grafico['x'],
                    yticklabels= self.grafico['y'],
                    **self.filter_kwargs())
    
    
    @decorator_filter_kw(['data','x','y'])
    def filter_kwargs(self):
        """
        Método decorado com @decorator_filter_kw para filtrar configurações específicas do gráfico.

        Retorna:
        - None
        """
        return None


class My_group_scatterplot(My_styles):
    """
    Classe que herda de My_styles e personaliza configurações para gráficos de dispersão em grupo.

    Parâmetros:
    - **kwargs: Argumentos adicionais de palavra-chave para personalizar ainda mais o estilo.

    Métodos:
    - __init__(**kwargs):
      Inicializa o objeto My_group_scatterplot com o tipo de estilo 'group_scatterplot' e parâmetros adicionais.

    - make():
      Método que cria um gráfico de dispersão em grupo usando Seaborn e matplotlib.

    - axis_max_value():
      Retorna os valores máximos dos eixos x e y do conjunto de dados.

    - axis(g):
      Configura os eixos do gráfico de dispersão em grupo.

    - filter_kwargs():
      Método decorado com @decorator_filter_kw para filtrar configurações específicas do gráfico.

    Exemplo de Uso:
    ```python
    # Criar um objeto My_group_scatterplot com estilos personalizados
    my_custom_group_scatterplot = My_group_scatterplot(titulo={'label': 'Meu Gráfico de Dispersão em Grupo'})

    # Chamar o método make para gerar o gráfico
    my_custom_group_scatterplot.make()
    ```

    """
    def __init__(self,**kwargs):
        super().__init__(type_style="group_scatterplot", **kwargs)


    def make(self):
        """
        Método que cria um gráfico de dispersão em grupo usando Seaborn e matplotlib.

        Retorna:
        - None
        """
        sns.reset_defaults()
        sns.set(**self.estilo if hasattr(self, 'estilo') and self.estilo else {})
        g = sns.FacetGrid(**self.filter_kwargs())
        g.map(sns.scatterplot, self.grafico["x"], self.grafico["y"], **self.map)
        g.set_axis_labels(**self.eixos)
        g.set_titles(**self.titulos)
        self.axis(g)
        plt.show()


    def axis_max_value(self):
        """
        Retorna os valores máximos dos eixos x e y do conjunto de dados.

        Retorna:
        - tuple: Valores máximos dos eixos x e y.
        """
        max_axis_x = self.grafico["data"][self.grafico["x"]].max()
        max_axis_y = self.grafico["data"][self.grafico["y"]].max()
        return max_axis_x,max_axis_y


    def axis(self,g):
        """
        Configura os eixos do gráfico de dispersão em grupo.

        Parâmetros:
        - g (seaborn.axisgrid.FacetGrid): Objeto que representa o gráfico de dispersão em grupo.

        Retorna:
        - None
        """
        for ax in g.axes.flat:
            max_axis = self.axis_max_value()
            ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: format_ticks(x, max_axis[0], p)))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, p: format_ticks(y, max_axis[1], p)))
            ax.tick_params(**self.tick_params_x)
            ax.tick_params(**self.tick_params_y)


    @decorator_filter_kw(['x','y'])
    def filter_kwargs(self): 
        """
        Método decorado com @decorator_filter_kw para filtrar configurações específicas do gráfico.

        Retorna:
        - None
        """
        return None



if __name__ == '__main__':
    print('Teste da classe: My_styles:')
    dict_boxplot = {"titulo": {"label": "Lorem Ipsum"}, "grafico": {"data": [[1, 2, 3, 4, 5]], "y": "Lorem Y"}}
    my_st = My_styles(type_style='boxplot', **dict_boxplot)
    print(repr(my_st.__dict__))
    
    print('-'*50)

    print('Teste da função fast_instance:')
    fast = fast_instance(data=[[1,2,3,4,5]],y="Lorem Y",title="Lorem Ipsum")
    my_st2 = My_styles(type_style='boxplot', **fast)
    print(repr(my_st2.__dict__))

