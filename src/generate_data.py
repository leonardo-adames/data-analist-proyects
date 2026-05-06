"""
generate_data.py
================
Genera un dataset sintético de ventas retail para el proyecto de análisis.
Simula 2 años de operaciones de una cadena de tiendas con patrones realistas.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

FECHA_INICIO = datetime(2023, 1, 1)
FECHA_FIN    = datetime(2024, 12, 31)
N_TRANSACCIONES = 15_000

TIENDAS = {
    "TDA-001": {"nombre": "Sucursal Centro",  "ciudad": "Santo Domingo", "zona": "Urbana"},
    "TDA-002": {"nombre": "Sucursal Norte",   "ciudad": "Santiago",      "zona": "Urbana"},
    "TDA-003": {"nombre": "Sucursal Este",    "ciudad": "San Pedro",     "zona": "Suburbana"},
    "TDA-004": {"nombre": "Sucursal Sur",     "ciudad": "Baní",          "zona": "Rural"},
    "TDA-005": {"nombre": "Sucursal Online",  "ciudad": "Nacional",      "zona": "Digital"},
}

CATEGORIAS = {
    "Electrónica":      {"precio_min": 500,  "precio_max": 25000, "margen": 0.18},
    "Electrodomésticos":{"precio_min": 800,  "precio_max": 40000, "margen": 0.22},
    "Celulares":        {"precio_min": 1200, "precio_max": 30000, "margen": 0.15},
    "Accesorios":       {"precio_min": 50,   "precio_max": 2000,  "margen": 0.45},
    "Computadoras":     {"precio_min": 5000, "precio_max": 80000, "margen": 0.20},
    "Audio/Video":      {"precio_min": 300,  "precio_max": 15000, "margen": 0.30},
    "Gaming":           {"precio_min": 400,  "precio_max": 12000, "margen": 0.25},
    "Hogar Inteligente":{"precio_min": 200,  "precio_max": 8000,  "margen": 0.35},
}

METODOS_PAGO = ["Efectivo", "Tarjeta Crédito", "Tarjeta Débito", "Transferencia", "Cuotas"]
VENDEDORES   = [f"VEN-{str(i).zfill(3)}" for i in range(1, 21)]

def generar_fechas(n):
    fechas = []
    dias_total = (FECHA_FIN - FECHA_INICIO).days
    for _ in range(n):
        dia_offset = int(np.random.triangular(0, dias_total * 0.7, dias_total))
        fecha = FECHA_INICIO + timedelta(days=dia_offset % dias_total)
        if fecha.month == 12 and random.random() < 0.35:
            fecha = fecha.replace(month=12, day=random.randint(1, 28))
        fechas.append(fecha)
    return sorted(fechas)

def generar_ventas():
    fechas     = generar_fechas(N_TRANSACCIONES)
    tienda_ids = random.choices(list(TIENDAS.keys()), weights=[30,25,20,10,15], k=N_TRANSACCIONES)
    categorias = random.choices(list(CATEGORIAS.keys()), weights=[20,15,18,12,10,8,10,7], k=N_TRANSACCIONES)

    rows = []
    for i, (fecha, tienda_id, categoria) in enumerate(zip(fechas, tienda_ids, categorias)):
        cfg = CATEGORIAS[categoria]
        precio_unitario = round(random.uniform(cfg["precio_min"], cfg["precio_max"]), 2)
        cantidad        = int(np.random.choice([1,2,3,4,5], p=[0.55,0.25,0.12,0.05,0.03]))
        descuento_pct   = round(random.choices([0,5,10,15,20,25], weights=[40,20,15,10,10,5])[0] / 100, 2)
        precio_final    = round(precio_unitario * cantidad * (1 - descuento_pct), 2)
        costo           = round(precio_final * (1 - cfg["margen"]), 2)
        ganancia        = round(precio_final - costo, 2)
        devolucion      = random.random() < 0.03
        tienda_info     = TIENDAS[tienda_id]
        rows.append({
            "id_transaccion":  f"TXN-{str(i+1).zfill(6)}",
            "fecha":           fecha.strftime("%Y-%m-%d"),
            "hora":            f"{random.randint(8,21):02d}:{random.choice(['00','15','30','45'])}",
            "tienda_id":       tienda_id,
            "tienda_nombre":   tienda_info["nombre"],
            "ciudad":          tienda_info["ciudad"],
            "zona":            tienda_info["zona"],
            "vendedor_id":     random.choice(VENDEDORES),
            "categoria":       categoria,
            "precio_unitario": precio_unitario,
            "cantidad":        cantidad,
            "descuento_pct":   descuento_pct,
            "total_venta":     precio_final,
            "costo":           costo,
            "ganancia_bruta":  ganancia,
            "margen_pct":      round(ganancia / precio_final * 100, 2) if precio_final > 0 else 0,
            "metodo_pago":     random.choice(METODOS_PAGO),
            "devolucion":      devolucion,
            "id_cliente":      f"CLI-{random.randint(1000, 9999)}",
        })

    df = pd.DataFrame(rows)
    df.loc[df["devolucion"], ["total_venta", "ganancia_bruta"]] *= -1
    return df

if __name__ == "__main__":
    os.makedirs("../data", exist_ok=True)
    df = generar_ventas()
    df.to_csv("../data/ventas_retail.csv", index=False, encoding="utf-8-sig")
    print(f"Dataset generado: {len(df):,} transacciones")
    print(f"Periodo: {df['fecha'].min()} a {df['fecha'].max()}")
    print(f"Revenue total: ${df['total_venta'].sum():,.2f}")
