def format_ticks(value, max=None, _=None):
    """
    Formata os rótulos dos ticks dos eixos com base nos valores e na escala máxima.

    Parâmetros:
    - value (float): Valor do tick a ser formatado.
    - max (float, opcional): Valor máximo da escala. Se não fornecido, assume o valor de 'value'.
    - _ (objeto, opcional): Parâmetro ignorado.

    Retorna:
    - str: Rótulo do tick formatado.

    Observações:
    - A função utiliza uma escala de formatação baseada em potências de 10 (mil, MM, B, T).
    - Se o valor máximo dividido pela unidade da escala estiver entre 0.1 e 999, a formatação é aplicada.
    - Se o `formatted_value` for menor que 1, a escala e a divisão são ajustadas para uma chave anterior no `scale_dict`.
    - Os rótulos são formatados como '{formatted_value:.0f}{escala}' (exceto para mil) ou '{formatted_value:.0f}'.

    Exemplo de Uso:
    ```python
    # Utilizar a função para formatar um tick em um gráfico
    formatted_tick = format_ticks(1234567, max=1000000)
    ```

    """
    if max is None:
        max = value

    if value == 0:
        return f'{value:.0f}'


    scale_dict = {
        "mil": 1e3,
        "MM": 1e6,
        "B": 1e9,
        "T": 1e12,
    }

    for scale, unidade in scale_dict.items():
        if 0.1 <= max / unidade < 999:
            formatted_value = value / scale_dict[scale]
            if formatted_value < 1:
                prev_scales = list(scale_dict.keys())
                index = prev_scales.index(scale) - 1
                prev_scale = prev_scales[index] if index > 0 else ''
                return f'{value:.0f}{prev_scale}'
            else:
                return f'{formatted_value:.0f}{scale}'

    return f'{value:.0f}'


def truncate_label(label: str, length=32):
    """
    Trunca uma string de rótulo para um comprimento específico, adicionando reticências se necessário.

    Args:
        label (str): String representando o rótulo a ser truncado.
        length (int): Comprimento desejado para o rótulo truncado. O padrão é 32.

    Returns:
        str: A string do rótulo truncado para o comprimento especificado, com reticências adicionadas se necessário.

    Example:
        label = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry'
        truncated_label = truncate_label(label, length=20)
        # Output:
        # 'Lorem Ipsum is sim...'
    """
    truncated_label = label[:length] + '...' if len(label) > length else label
    return truncated_label


if __name__ == '__main__':
    print('Teste format_ticks:')
    f_ticks = format_ticks(value=1e7, max=1e8, _='')
    print(f_ticks)

    
    print('---------------------')

    
    lorem="""Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s"""
    print('Teste truncate_label:')
    trun_l = truncate_label(label=lorem)
    print(trun_l)