import streamlit as st

# Título de la calculadora
st.title("Calculadora de Método Secuencial con Apuestas Combinadas")

# Primer apartado: DATOS COMBINADA
st.header("DATOS COMBINADA")

# Campo Selecciones
selecciones = st.selectbox("Selecciones", ["2", "3"])

# Campo Tipo de Apuesta
tipo_apuesta = st.selectbox("Tipo de Apuesta", ["Dinero Real", "Freebet", "Reembolso"])

# Campo Cuota a Favor
cuota_combinada = st.number_input("Cuota a Favor (Combinada)", min_value=1.0, value=2.0, step=0.01)

# Campo Importe de la Apuesta
importe_apuesta = st.number_input("Importe de la Apuesta (EUR)", min_value=0.0, value=10.0, step=0.1)

# Campo Retención (visible sólo para Freebet y Reembolso)
if tipo_apuesta in ["Freebet", "Reembolso"]:
    retencion = st.number_input("Retención (%)", min_value=0.0, max_value=100.0, value=70.0, step=1.0)

# Campo Reembolso (visible sólo para Reembolso)
if tipo_apuesta == "Reembolso":
    reembolso = st.number_input("Reembolso (EUR)", min_value=0.0, value=5.0, step=0.1)

# Segundo apartado: APUESTAS EXCHANGE
st.header("APUESTAS EXCHANGE")

# Línea 1
st.write("Línea 1")
cuota_1 = st.number_input("Cuota 1", min_value=1.0, value=2.0, step=0.01)
comision_1 = 2.0  # Comisión fija del 2%

# Línea 2
st.write("Línea 2")
cuota_2 = st.number_input("Cuota 2", min_value=1.0, value=2.0, step=0.01)
comision_2 = 2.0  # Comisión fija del 2%

# Línea 3 (visible sólo si se seleccionan 3 selecciones)
cuota_3 = None
if selecciones == "3":
    st.write("Línea 3")
    cuota_3 = st.number_input("Cuota 3", min_value=1.0, value=2.0, step=0.01)
    comision_3 = 2.0  # Comisión fija del 2%

# Calcular Importe Lay 1 en función del tipo de apuesta y número de selecciones
if tipo_apuesta == "Dinero Real":
    if selecciones == "2":
        importe_lay_1 = round((importe_apuesta * cuota_combinada) / ((cuota_1 * cuota_2) - 0.02), 2)
    else:
        importe_lay_1 = round((importe_apuesta * cuota_combinada) / ((cuota_1 * cuota_2 * cuota_3) - 0.02), 2)

elif tipo_apuesta == "Freebet":
    if selecciones == "2":
        importe_lay_1 = round((importe_apuesta * (cuota_combinada - 1)) / ((cuota_1 * cuota_2) - 0.02), 2)
    else:
        importe_lay_1 = round((importe_apuesta * (cuota_combinada - 1)) / ((cuota_1 * cuota_2 * cuota_3) - 0.02), 2)

elif tipo_apuesta == "Reembolso":
    if selecciones == "2":
        importe_lay_1 = round((importe_apuesta * (cuota_combinada - (reembolso / importe_apuesta) * (retencion / 100))) / (cuota_1 * cuota_2), 2)
    else:
        importe_lay_1 = round((importe_apuesta * (cuota_combinada - (reembolso / importe_apuesta) * (retencion / 100))) / (cuota_1 * cuota_2 * cuota_3), 2)

st.write(f"Importe Lay 1: {importe_lay_1} EUR")

# Calcular Riesgo 1: fórmula IMPORTE LAY 1 * (CUOTA 1 - 1)
riesgo_1 = round(importe_lay_1 * (cuota_1 - 1), 2)
st.write(f"Riesgo 1: {riesgo_1} EUR")

# Importe Lay 2: Suma de Importe Lay 1 + Riesgo 1
importe_lay_2 = round(importe_lay_1 + riesgo_1, 2)
st.write(f"Importe Lay 2: {importe_lay_2} EUR")

# Calcular Riesgo 2: fórmula IMPORTE LAY 2 * (CUOTA 2 - 1)
riesgo_2 = round(importe_lay_2 * (cuota_2 - 1), 2)
st.write(f"Riesgo 2: {riesgo_2} EUR")

# Calcular para la Línea 3 si está seleccionada
if selecciones == "3":
    # Importe Lay 3: Suma de Importe Lay 2 + Riesgo 2
    importe_lay_3 = round(importe_lay_2 + riesgo_2, 2)
    st.write(f"Importe Lay 3: {importe_lay_3} EUR")

    # Calcular Riesgo 3: fórmula IMPORTE LAY 3 * (CUOTA 3 - 1)
    riesgo_3 = round(importe_lay_3 * (cuota_3 - 1), 2)
    st.write(f"Riesgo 3: {riesgo_3} EUR")

# Tercer apartado: RESULTADO
st.header("RESULTADO")

if st.button("Calcular"):
    if tipo_apuesta == "Dinero Real":
        # Dinero Real
        resultado_gano_combinada = round(importe_apuesta * (cuota_combinada - 1) - riesgo_1 - riesgo_2 - (riesgo_3 if selecciones == "3" else 0), 2)
        resultado_pierdo_1_apuesta = round((importe_lay_1 * 0.98) - importe_apuesta, 2)
        resultado_pierdo_2_apuesta = round((importe_lay_2 * 0.98) - riesgo_1 - importe_apuesta, 2)
        
        st.write(f"GANO LA COMBINADA EN LA BOOKIE: {resultado_gano_combinada} EUR")
        st.write(f"PIERDO 1ª APUESTA Y GANO 1ª CONTRA: {resultado_pierdo_1_apuesta} EUR")
        st.write(f"PIERDO 2ª APUESTA Y GANO 2ª CONTRA: {resultado_pierdo_2_apuesta} EUR")
        
        if selecciones == "3":
            resultado_pierdo_3_apuesta = round((importe_lay_3 * 0.98) - riesgo_2 - riesgo_1 - importe_apuesta, 2)
            st.write(f"PIERDO 3ª APUESTA Y GANO 3ª CONTRA: {resultado_pierdo_3_apuesta} EUR")
    
    elif tipo_apuesta == "Freebet":
        # Freebet
        resultado_gano_combinada = round(importe_apuesta * (cuota_combinada - 1) - riesgo_1 - riesgo_2 - (riesgo_3 if selecciones == "3" else 0), 2)
        resultado_pierdo_1_apuesta = round(importe_lay_1 * 0.98, 2)
        resultado_pierdo_2_apuesta = round((importe_lay_2 * 0.98) - riesgo_1, 2)
        
        st.write(f"GANO LA COMBINADA EN LA BOOKIE: {resultado_gano_combinada} EUR")
        st.write(f"PIERDO 1ª APUESTA Y GANO 1ª CONTRA: {resultado_pierdo_1_apuesta} EUR")
        st.write(f"PIERDO 2ª APUESTA Y GANO 2ª CONTRA: {resultado_pierdo_2_apuesta} EUR")
        
        if selecciones == "3":
            resultado_pierdo_3_apuesta = round((importe_lay_3 * 0.98) - riesgo_2 - riesgo_1, 2)
            st.write(f"PIERDO 3ª APUESTA Y GANO 3ª CONTRA: {resultado_pierdo_3_apuesta} EUR")
    
    elif tipo_apuesta == "Reembolso":
        # Reembolso
        resultado_gano_combinada = round(importe_apuesta * (cuota_combinada - 1) - riesgo_1 - riesgo_2 - (riesgo_3 if selecciones == "3" else 0), 2)
        resultado_pierdo_1_apuesta = round(((importe_lay_1 * 0.98) - importe_apuesta) + (reembolso * (retencion / 100)), 2)
        resultado_pierdo_2_apuesta = round(((importe_lay_2 * 0.98) - riesgo_1 - importe_apuesta) + (reembolso * (retencion / 100)), 2)
        
        st.write(f"GANO LA COMBINADA EN LA BOOKIE: {resultado_gano_combinada} EUR")
        st.write(f"PIERDO 1ª APUESTA Y GANO 1ª CONTRA: {resultado_pierdo_1_apuesta} EUR")
        st.write(f"PIERDO 2ª APUESTA Y GANO 2ª CONTRA: {resultado_pierdo_2_apuesta} EUR")
        
        if selecciones == "3":
            resultado_pierdo_3_apuesta = round(((importe_lay_3 * 0.98) - riesgo_2 - riesgo_1 - importe_apuesta) + (reembolso * (retencion / 100)), 2)
            st.write(f"PIERDO 3ª APUESTA Y GANO 3ª CONTRA: {resultado_pierdo_3_apuesta} EUR")



