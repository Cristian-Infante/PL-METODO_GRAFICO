import tkinter as tk
import sympy as sym
import numpy as np
import matplotlib.pyplot as plt

def getMaxX(puntos):
    max_x = 0
    for p in puntos:
        if len(p) > 0:
            x = sym.Symbol("x")
            if p[0].get(x) > max_x:
                max_x = p[0].get(x)
    return max_x

def getMaxY(puntos):
    max_y = 0
    for p in puntos:
        if len(p) > 0:
            y = sym.Symbol("y")
            if p[0].get(y) > max_y:
                max_y = p[0].get(y)
    return max_y

def isPuntoInList(x_c, y_c, lista):
    x = sym.Symbol("x")
    y = sym.Symbol("y")
    for point in lista:
        if len(point) > 0 and point[0].get(x) == x_c and point[0].get(y) == y_c:
            return True
    return False

def getPuntos(ec_despejadas, u_ecuacion=[]):
    puntos = list()
    puntos_filtrados = list()
    expresion = ""
    for i, el in enumerate(ec_despejadas):
        for j, ec in enumerate(ec_despejadas):
            if i == j:
                continue
            puntos_solve = sym.solve([el, ec], dict=True)
            puntos.append(puntos_solve)
    
    for i in u_ecuacion:
        expresion += i + " and "
    
    expresion = expresion[:-5]

    x = sym.Symbol("x")
    y = sym.Symbol("y")
    lista_puntos_sin_vacio = [elem for elem in puntos if elem]
    puntos_filtrados = [punto for punto in lista_puntos_sin_vacio if eval(expresion, {"x": punto[0].get(x), "y": punto[0].get(y)})]
    
    puntos_filtrados_unicos = []
    for i, p_filtrado in enumerate(puntos_filtrados):
        if not isPuntoInList(p_filtrado[0].get(x), p_filtrado[0].get(y), puntos_filtrados_unicos):
            puntos_filtrados_unicos.append(p_filtrado)

    return puntos_filtrados_unicos

def maxZ(puntos, e_beneficio):
    x = sym.Symbol("x")
    y = sym.Symbol("y")
    maxima_ganancia = 0
    iteracion = 1
    for punto in puntos:
        ganancia = eval(e_beneficio, {'x': punto[0].get(x), 'y': punto[0].get(y)})
        if ganancia >= maxima_ganancia:
            maxima_ganancia = ganancia
        iteracion = 1 + iteracion
    return maxima_ganancia

def minZ(puntos, e_costo):
    x = sym.Symbol("x")
    y = sym.Symbol("y")
    minimo_costo = float('inf')
    iteracion = 1
    for punto in puntos:
        costo = eval(e_costo, {'x': punto[0].get(x), 'y': punto[0].get(y)})
        if costo <= minimo_costo:
            minimo_costo = costo
        iteracion = 1 + iteracion
    return minimo_costo

def showViablePointsAndProfit (puntos, e_objetivo, maximize=True):
    x = sym.Symbol("x")
    y = sym.Symbol("y")
    if maximize:
        max_valor = maxZ(puntos, e_objetivo)
    else:
        max_valor = minZ(puntos, e_objetivo)
    
    points_text = "\n"
    for punto in puntos:
        x_value = punto[0].get(x)
        y_value = punto[0].get(y)
        valor = eval(e_objetivo, {'x': x_value, 'y': y_value})
        
        if x_value != int(x_value) or y_value != int(y_value) or valor != int(valor):
            x_value = round(x_value, 2)
            y_value = round(y_value, 2)
            valor = round(valor, 2)
        
        points_text += f"x = {x_value} \t y = {y_value} \n-> Ganancia = ${valor}\n\n"
    
    if max_valor != int(max_valor):
        max_valor = round(max_valor, 2)
    
    if maximize:
        points_text += f"Ganancia máxima posible es: ${max_valor}"
    else:
        points_text += f"Ganancia mínima posible es: ${max_valor}"
    
    result_label.config(text=points_text)

def transformList(lista_de_diccionarios):
    x = sym.Symbol("x")
    y = sym.Symbol("y")
    intersecciones = []
    
    for diccionario in lista_de_diccionarios:
        x_val = diccionario[0].get(x)
        y_val = diccionario[0].get(y)
        
        if x_val is not None and y_val is not None:
            intersecciones.append([float(x_val), float(y_val)])  # Convert values to float
    
    if len(intersecciones) == 0:
        return None
    
    intersecciones_np = np.array(intersecciones)
    
    # Obtener los índices que ordenarían la lista
    orden_indices = np.lexsort((intersecciones_np[:, 1], intersecciones_np[:, 0]))
    
    # Aplicar el orden a la lista resultante
    intersecciones_ordenadas = intersecciones_np[orden_indices]
    
    return intersecciones_ordenadas

def graph(ecuaciones, intersecciones):
    puntos = intersecciones
    # print(puntos)
    intersecciones = transformList(puntos)
    # print(intersecciones)
    # Definir símbolos x e y
    x, y = sym.symbols('x y')

    plt.figure(figsize=(8, 8))

    for ecuacion in ecuaciones:
        # Limpiar espacios en blanco y dividir la ecuación en partes
        formula = ecuacion
        ecuacion = ecuacion.replace(" ", "")
        partes = ecuacion.split('=')

        if len(partes) != 2:
            print(f"Error: La ecuación '{ecuacion}' no está en el formato correcto.")
            continue

        # Resolver la ecuación para obtener la ecuación resuelta en la forma 'y = mx + b'
        try:
            eq = sym.Eq(sym.S(partes[0]), sym.S(partes[1]))
            ecuacion_resuelta = sym.solve(eq, y)[0]
        except (sym.SympifyError, ValueError, TypeError):
            print(f"Error: La ecuación '{ecuacion}' no está en el formato correcto.")
            continue

        # Calcular los valores correspondientes de y usando los puntos de intersección proporcionados
        x_values = intersecciones[:, 0]
        y_values = np.array([ecuacion_resuelta.subs(x, val).evalf() for val in x_values])

        # Graficar la ecuación en la figura actual
        plt.plot(x_values, y_values, label=f'{formula}')

    # Agregar restricciones x >= 0 y >= 0 usando axvline y axhline
    plt.axvline(x=0, color='green', label='x >= 0')
    plt.axhline(y=0, color='green', label='y >= 0')
    
    # Graficar los puntos de intersección
    # print(puntos)
    for punto in puntos:
        x = sym.Symbol("x")
        y = sym.Symbol("y")
        if len(punto) > 0:
            plt.plot(punto[0].get(x), punto[0].get(y), marker="o")
            plt.text(punto[0].get(x), punto[0].get(y), f"{punto[0].get(x)},{punto[0].get(y)}")
    
    # Rellenar el área entre los puntos de intersección
    plt.fill_between(intersecciones[:, 0], 0, intersecciones[:, 1], color='gray', alpha=0.5)

    # Personalizar el gráfico
    plt.title('Gráfico - Restricciones y puntos viables')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.grid(True)
    plt.legend()

    # Mostrar el gráfico
    plt.show()

def calculateProfit():
    e_objetivo = entry_objetivo.get()
    u_ecuaciones = entry_ecuaciones.get("1.0", "end-1c").splitlines()
    ecuacionesGraficas = []
    ec_despejadas = []
    
    maximize = True if optimization_var.get() == 1 else False

    for ec_inicial in u_ecuaciones:
        ec_inicial = ec_inicial.replace("<=", "=")
        ec_inicial = ec_inicial.replace(">=", "=")

        ec_split = ec_inicial.split("=")

        ec_var = ec_split[0]
        ec_expr = ec_split[1]
        ec_grafica = ec_var + "=" + ec_expr
        ecuacionesGraficas.append(ec_grafica)
        ec_final = ec_var + "-" + ec_expr
        ec_despejadas.append(ec_final)
    
    ec_despejadas.append("x-0")
    ec_despejadas.append("y-0")

    puntos_interseccion = getPuntos(ec_despejadas, u_ecuaciones)
    
    showViablePointsAndProfit (puntos_interseccion, e_objetivo, maximize)
    # print(ecuacionesGraficas)
    graph(ecuacionesGraficas, puntos_interseccion)

# Create the tkinter window
window = tk.Tk()
window.title("Calculadora de Programación Lineal")

# Create and configure input widgets
objetivo_label = tk.Label(window, text="Ingrese la función objetivo:")
objetivo_label.pack()

entry_objetivo = tk.Entry(window)
entry_objetivo.pack()

equations_label = tk.Label(window, text="Ingrese las restricciones (una por línea):")
equations_label.pack()

entry_ecuaciones = tk.Text(window, height=5, width=30)
entry_ecuaciones.pack()

optimization_label = tk.Label(window, text="Seleccione la dirección de la optimización:")
optimization_label.pack()

optimization_var = tk.IntVar()
maximize_radio = tk.Radiobutton(window, text="Maximizar", variable=optimization_var, value=1)
minimize_radio = tk.Radiobutton(window, text="Minimizar", variable=optimization_var, value=2)
maximize_radio.pack()
minimize_radio.pack()

calculate_button = tk.Button(window, text="Calcular", command=calculateProfit)
calculate_button.pack()

result_label = tk.Label(window, text="", justify=tk.CENTER)
result_label.pack()

# Start the tkinter main loop
window.mainloop()
