# %% [markdown]
# # Análisis de Ventas Retail — Cadena de Tiendas 2023–2024
# **Proyecto:** Retail Sales Intelligence Dashboard  
# **Autor:** Leonardo (Aizen) — Bootcamp Business Intelligence  
# **Dataset:** 15,000 transacciones reales simuladas | 5 tiendas | 8 categorías  
#
# ---
# ## Objetivo del proyecto
# Identificar patrones de revenue, rentabilidad por categoría, comportamiento
# estacional y desempeño por tienda para apoyar decisiones comerciales reales.

# %% [markdown]
# ## 1. Importaciones y configuración

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
import os

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.max_columns", 20)

# Paleta profesional consistente en todo el notebook
PALETTE = {
    "primary":    "#1B4F72",
    "secondary":  "#2E86C1",
    "accent":     "#E74C3C",
    "success":    "#1E8449",
    "warning":    "#D4AC0D",
    "neutral":    "#566573",
    "bg":         "#F8F9FA",
    "categorical": ["#1B4F72","#2E86C1","#1E8449","#D4AC0D","#E74C3C","#7D3C98","#CA6F1E","#117A65"],
}

plt.rcParams.update({
    "figure.facecolor":  PALETTE["bg"],
    "axes.facecolor":    "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.grid":         True,
    "grid.alpha":        0.3,
    "grid.linestyle":    "--",
    "font.family":       "DejaVu Sans",
    "font.size":         11,
})

os.makedirs("../outputs", exist_ok=True)
print("✅ Configuración lista")

# %% [markdown]
# ## 2. Carga y exploración inicial del dataset

# %%
df = pd.read_csv("../data/ventas_retail.csv", encoding="utf-8-sig")
df["fecha"]     = pd.to_datetime(df["fecha"])
df["año"]       = df["fecha"].dt.year
df["mes"]       = df["fecha"].dt.month
df["mes_nombre"]= df["fecha"].dt.strftime("%b")
df["trimestre"] = df["fecha"].dt.quarter
df["dia_semana"]= df["fecha"].dt.day_name()
df["semana"]    = df["fecha"].dt.isocalendar().week.astype(int)

print(f"Shape: {df.shape}")
print(f"\nPeriodo: {df['fecha'].min().date()} → {df['fecha'].max().date()}")
print(f"\nTipos de datos:\n{df.dtypes}")

# %%
# Resumen ejecutivo del dataset
ventas_limpias = df[df["total_venta"] > 0]  # Excluye devoluciones para KPIs

print("=" * 55)
print("       RESUMEN EJECUTIVO — VENTAS RETAIL")
print("=" * 55)
print(f"  Total transacciones:     {len(df):>12,}")
print(f"  Transacciones positivas: {len(ventas_limpias):>12,}")
print(f"  Devoluciones:            {df['devolucion'].sum():>12,}")
print(f"  Revenue bruto:           ${ventas_limpias['total_venta'].sum():>13,.0f}")
print(f"  Ganancia bruta:          ${ventas_limpias['ganancia_bruta'].sum():>13,.0f}")
print(f"  Ticket promedio:         ${ventas_limpias['total_venta'].mean():>13,.0f}")
print(f"  Margen promedio:         {ventas_limpias['margen_pct'].mean():>12.1f}%")
print(f"  Clientes únicos:         {df['id_cliente'].nunique():>12,}")
print(f"  Vendedores activos:      {df['vendedor_id'].nunique():>12,}")
print("=" * 55)

# %% [markdown]
# ## 3. Análisis de Revenue — Tendencia Mensual

# %%
revenue_mensual = (
    ventas_limpias
    .groupby(["año", "mes", "mes_nombre"])["total_venta"]
    .sum()
    .reset_index()
    .sort_values(["año", "mes"])
)
revenue_mensual["total_millones"] = revenue_mensual["total_venta"] / 1_000_000

fig, axes = plt.subplots(2, 1, figsize=(14, 10), facecolor=PALETTE["bg"])
fig.suptitle("Análisis de Revenue Mensual — 2023 vs 2024", 
             fontsize=16, fontweight="bold", y=0.98, color=PALETTE["primary"])

# Subplot 1: línea de tendencia por año
ax1 = axes[0]
for año, color in zip([2023, 2024], [PALETTE["secondary"], PALETTE["accent"]]):
    datos = revenue_mensual[revenue_mensual["año"] == año]
    ax1.plot(datos["mes"], datos["total_millones"], 
             marker="o", linewidth=2.5, markersize=7,
             label=str(año), color=color)
    ax1.fill_between(datos["mes"], datos["total_millones"], 
                     alpha=0.08, color=color)

ax1.set_xlabel("Mes")
ax1.set_ylabel("Revenue (millones RD$)")
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(["Ene","Feb","Mar","Abr","May","Jun",
                      "Jul","Ago","Sep","Oct","Nov","Dic"])
ax1.legend(frameon=False, fontsize=11)
ax1.set_title("Tendencia mensual comparativa", pad=10, color=PALETTE["neutral"])

# Subplot 2: barras apiladas por año
ax2 = axes[1]
x = np.arange(12)
width = 0.35
for i, (año, color) in enumerate(zip([2023, 2024], [PALETTE["secondary"], PALETTE["accent"]])):
    datos = revenue_mensual[revenue_mensual["año"] == año]["total_millones"].values
    bars = ax2.bar(x + i*width, datos, width, label=str(año), color=color, alpha=0.85)
    for bar, val in zip(bars, datos):
        if val > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                     f"{val:.1f}M", ha="center", va="bottom", fontsize=8, color=PALETTE["neutral"])

ax2.set_xticks(x + width/2)
ax2.set_xticklabels(["Ene","Feb","Mar","Abr","May","Jun",
                      "Jul","Ago","Sep","Oct","Nov","Dic"])
ax2.set_ylabel("Revenue (millones RD$)")
ax2.legend(frameon=False)
ax2.set_title("Revenue mensual por año", pad=10, color=PALETTE["neutral"])

plt.tight_layout()
plt.savefig("../outputs/01_revenue_mensual.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Gráfico guardado: 01_revenue_mensual.png")

# %% [markdown]
# ## 4. Análisis por Categoría — Revenue y Rentabilidad

# %%
cat_resumen = (
    ventas_limpias
    .groupby("categoria")
    .agg(
        revenue       = ("total_venta",    "sum"),
        ganancia      = ("ganancia_bruta", "sum"),
        transacciones = ("id_transaccion", "count"),
        ticket_prom   = ("total_venta",    "mean"),
        margen_prom   = ("margen_pct",     "mean"),
    )
    .assign(
        revenue_M     = lambda x: x["revenue"] / 1_000_000,
        ganancia_M    = lambda x: x["ganancia"] / 1_000_000,
        participacion = lambda x: (x["revenue"] / x["revenue"].sum() * 100).round(1),
    )
    .sort_values("revenue", ascending=False)
    .reset_index()
)

print(cat_resumen[["categoria","revenue_M","margen_prom","participacion","transacciones"]].to_string(index=False))

# %%
fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=PALETTE["bg"])
fig.suptitle("Rentabilidad por Categoría de Producto", 
             fontsize=15, fontweight="bold", color=PALETTE["primary"])

colores = PALETTE["categorical"][:len(cat_resumen)]

# Gráfico 1: Revenue por categoría
ax1 = axes[0]
bars = ax1.barh(cat_resumen["categoria"][::-1], 
                cat_resumen["revenue_M"][::-1], 
                color=colores[::-1], alpha=0.85)
ax1.set_xlabel("Revenue (millones RD$)")
ax1.set_title("Revenue total", fontweight="bold", color=PALETTE["neutral"])
for bar, val in zip(bars, cat_resumen["revenue_M"][::-1]):
    ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f"${val:.1f}M", va="center", fontsize=9)

# Gráfico 2: Margen promedio
ax2 = axes[1]
bars2 = ax2.barh(cat_resumen["categoria"][::-1],
                 cat_resumen["margen_prom"][::-1],
                 color=colores[::-1], alpha=0.85)
ax2.set_xlabel("Margen promedio (%)")
ax2.set_title("Margen de ganancia", fontweight="bold", color=PALETTE["neutral"])
ax2.axvline(cat_resumen["margen_prom"].mean(), color=PALETTE["accent"],
            linestyle="--", alpha=0.7, label=f"Prom: {cat_resumen['margen_prom'].mean():.1f}%")
ax2.legend(frameon=False, fontsize=9)

# Gráfico 3: Bubble chart Revenue vs Margen
ax3 = axes[2]
scatter = ax3.scatter(
    cat_resumen["margen_prom"],
    cat_resumen["revenue_M"],
    s=cat_resumen["transacciones"] / 5,
    c=colores[:len(cat_resumen)],
    alpha=0.8, edgecolors="white", linewidth=1.5
)
for _, row in cat_resumen.iterrows():
    ax3.annotate(row["categoria"], 
                 (row["margen_prom"], row["revenue_M"]),
                 textcoords="offset points", xytext=(6, 4), fontsize=8)
ax3.set_xlabel("Margen promedio (%)")
ax3.set_ylabel("Revenue (millones RD$)")
ax3.set_title("Revenue vs Margen\n(tamaño = n° transacciones)", 
              fontweight="bold", color=PALETTE["neutral"])

plt.tight_layout()
plt.savefig("../outputs/02_analisis_categorias.png", dpi=150, bbox_inches="tight")
plt.show()
print("✅ Gráfico guardado: 02_analisis_categorias.png")

# %% [markdown]
# ## 5. Desempeño por Tienda

# %%
tienda_resumen = (
    ventas_limpias
    .groupby(["tienda_id","tienda_nombre","zona"])
    .agg(
        revenue       = ("total_venta",    "sum"),
        ganancia      = ("ganancia_bruta", "sum"),
        transacciones = ("id_transaccion", "count"),
        ticket_prom   = ("total_venta",    "mean"),
        margen_prom   = ("margen_pct",     "mean"),
        clientes      = ("id_cliente",     "nunique"),
    )
    .assign(revenue_M = lambda x: x["revenue"] / 1_000_000)
    .sort_values("revenue", ascending=False)
    .reset_index()
)

fig, axes = plt.subplots(1, 2, figsize=(15, 6), facecolor=PALETTE["bg"])
fig.suptitle("Desempeño Comparativo por Tienda", 
             fontsize=15, fontweight="bold", color=PALETTE["primary"])

colores_tienda = PALETTE["categorical"][:len(tienda_resumen)]

# Revenue y Ganancia por tienda
ax1 = axes[0]
x    = np.arange(len(tienda_resumen))
w    = 0.35
b1   = ax1.bar(x - w/2, tienda_resumen["revenue_M"], w, 
               color=PALETTE["secondary"], label="Revenue", alpha=0.85)
b2   = ax1.bar(x + w/2, tienda_resumen["ganancia"] / 1e6, w,
               color=PALETTE["success"], label="Ganancia", alpha=0.85)
ax1.set_xticks(x)
ax1.set_xticklabels(tienda_resumen["tienda_nombre"], rotation=20, ha="right", fontsize=9)
ax1.set_ylabel("Millones RD$")
ax1.set_title("Revenue vs Ganancia", fontweight="bold", color=PALETTE["neutral"])
ax1.legend(frameon=False)

# Ticket promedio y margen
ax2 = axes[1]
color_map = {t: c for t, c in zip(tienda_resumen["tienda_id"], colores_tienda)}
scatter = ax2.scatter(
    tienda_resumen["ticket_prom"],
    tienda_resumen["margen_prom"],
    s=tienda_resumen["transacciones"] / 3,
    c=colores_tienda, alpha=0.85,
    edgecolors="white", linewidth=2, zorder=5
)
for _, row in tienda_resumen.iterrows():
    ax2.annotate(row["tienda_nombre"].replace("Sucursal ",""),
                 (row["ticket_prom"], row["margen_prom"]),
                 textcoords="offset points", xytext=(8, 5), fontsize=9,
                 color=PALETTE["primary"])
ax2.set_xlabel("Ticket promedio (RD$)")
ax2.set_ylabel("Margen promedio (%)")
ax2.set_title("Ticket vs Margen\n(tamaño = n° transacciones)",
              fontweight="bold", color=PALETTE["neutral"])
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig("../outputs/03_desempeno_tiendas.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 6. Análisis de Estacionalidad y Patrones Temporales

# %%
# Heatmap: Revenue por día de la semana y mes
pivot_heatmap = (
    ventas_limpias
    .groupby(["dia_semana", "mes"])["total_venta"]
    .sum()
    .unstack()
    .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    / 1_000_000
)
pivot_heatmap.index = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
pivot_heatmap.columns = ["Ene","Feb","Mar","Abr","May","Jun",
                          "Jul","Ago","Sep","Oct","Nov","Dic"]

fig, axes = plt.subplots(1, 2, figsize=(16, 5), facecolor=PALETTE["bg"])
fig.suptitle("Patrones Estacionales de Ventas", 
             fontsize=15, fontweight="bold", color=PALETTE["primary"])

# Heatmap
sns.heatmap(pivot_heatmap, ax=axes[0], cmap="Blues", 
            fmt=".1f", annot=True, linewidths=0.5,
            cbar_kws={"label": "Revenue (M RD$)"})
axes[0].set_title("Revenue por día y mes (M RD$)", 
                  fontweight="bold", color=PALETTE["neutral"])

# Revenue por trimestre y categoría
pivot_trim = (
    ventas_limpias
    .groupby(["trimestre","categoria"])["total_venta"]
    .sum().unstack() / 1_000_000
)
pivot_trim.index = ["Q1","Q2","Q3","Q4"]
pivot_trim.plot(kind="bar", ax=axes[1], color=PALETTE["categorical"], 
                alpha=0.85, width=0.7)
axes[1].set_title("Revenue por trimestre y categoría", 
                  fontweight="bold", color=PALETTE["neutral"])
axes[1].set_xlabel("Trimestre")
axes[1].set_ylabel("Revenue (M RD$)")
axes[1].legend(bbox_to_anchor=(1.01, 1), borderaxespad=0, frameon=False, fontsize=8)
axes[1].tick_params(axis="x", rotation=0)

plt.tight_layout()
plt.savefig("../outputs/04_estacionalidad.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 7. Análisis de Clientes — Segmentación RFM

# %%
# Calcula métricas RFM por cliente
fecha_referencia = ventas_limpias["fecha"].max() + pd.Timedelta(days=1)

rfm = (
    ventas_limpias
    .groupby("id_cliente")
    .agg(
        recencia       = ("fecha",        lambda x: (fecha_referencia - x.max()).days),
        frecuencia     = ("id_transaccion","count"),
        valor_monetario= ("total_venta",  "sum"),
    )
    .reset_index()
)

# Puntajes RFM (1–4)
rfm["R"] = pd.qcut(rfm["recencia"],       4, labels=[4,3,2,1]).astype(int)
rfm["F"] = pd.qcut(rfm["frecuencia"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
rfm["M"] = pd.qcut(rfm["valor_monetario"],4, labels=[1,2,3,4]).astype(int)
rfm["RFM_Score"] = rfm["R"] + rfm["F"] + rfm["M"]

# Segmentación
def segmentar_rfm(score):
    if score >= 10: return "Champions"
    elif score >= 8: return "Leales"
    elif score >= 6: return "Potenciales"
    elif score >= 4: return "En Riesgo"
    else: return "Perdidos"

rfm["Segmento"] = rfm["RFM_Score"].apply(segmentar_rfm)

seg_resumen = (
    rfm.groupby("Segmento")
    .agg(clientes=("id_cliente","count"),
         valor_prom=("valor_monetario","mean"),
         frecuencia_prom=("frecuencia","mean"))
    .reset_index()
    .sort_values("valor_prom", ascending=False)
)

print("\n📊 SEGMENTACIÓN RFM DE CLIENTES")
print(seg_resumen.to_string(index=False))

# %%
colores_seg = {
    "Champions": "#1B4F72",
    "Leales":    "#2E86C1",
    "Potenciales":"#1E8449",
    "En Riesgo": "#D4AC0D",
    "Perdidos":  "#E74C3C",
}

fig, axes = plt.subplots(1, 3, figsize=(18, 6), facecolor=PALETTE["bg"])
fig.suptitle("Segmentación RFM de Clientes", 
             fontsize=15, fontweight="bold", color=PALETTE["primary"])

# Donut de distribución de segmentos
ax1 = axes[0]
sizes = seg_resumen["clientes"].values
labels = seg_resumen["Segmento"].values
colors = [colores_seg[s] for s in labels]
wedges, texts, autotexts = ax1.pie(
    sizes, labels=labels, colors=colors,
    autopct="%1.1f%%", pctdistance=0.8,
    wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_fontsize(9)
ax1.set_title("Distribución de clientes", fontweight="bold", color=PALETTE["neutral"])

# Valor promedio por segmento
ax2 = axes[1]
bars = ax2.bar(seg_resumen["Segmento"], 
               seg_resumen["valor_prom"] / 1000,
               color=[colores_seg[s] for s in seg_resumen["Segmento"]], alpha=0.85)
for bar, val in zip(bars, seg_resumen["valor_prom"]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"${val:,.0f}", ha="center", fontsize=8, color=PALETTE["neutral"])
ax2.set_ylabel("Valor promedio (miles RD$)")
ax2.set_title("Valor monetario por segmento", fontweight="bold", color=PALETTE["neutral"])
ax2.tick_params(axis="x", rotation=15)

# Scatter Recencia vs Frecuencia
ax3 = axes[2]
for seg, color in colores_seg.items():
    sub = rfm[rfm["Segmento"] == seg]
    ax3.scatter(sub["recencia"], sub["frecuencia"],
                c=color, alpha=0.5, s=25, label=seg)
ax3.set_xlabel("Recencia (días desde última compra)")
ax3.set_ylabel("Frecuencia (n° transacciones)")
ax3.set_title("Recencia vs Frecuencia", fontweight="bold", color=PALETTE["neutral"])
ax3.legend(frameon=False, fontsize=8)

plt.tight_layout()
plt.savefig("../outputs/05_segmentacion_rfm.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 8. Análisis de Descuentos e Impacto en Rentabilidad

# %%
desc_impacto = (
    ventas_limpias
    .groupby("descuento_pct")
    .agg(
        transacciones = ("id_transaccion","count"),
        revenue_prom  = ("total_venta",   "mean"),
        margen_prom   = ("margen_pct",    "mean"),
    )
    .reset_index()
)

fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=PALETTE["bg"])
fig.suptitle("Impacto de Descuentos en Revenue y Margen",
             fontsize=15, fontweight="bold", color=PALETTE["primary"])

ax1 = axes[0]
ax1.bar([f"{int(d*100)}%" for d in desc_impacto["descuento_pct"]],
        desc_impacto["transacciones"],
        color=PALETTE["secondary"], alpha=0.85)
ax1.set_xlabel("Descuento aplicado")
ax1.set_ylabel("Número de transacciones")
ax1.set_title("Distribución de descuentos", fontweight="bold", color=PALETTE["neutral"])

ax2 = axes[1]
ax2_twin = ax2.twinx()
x_pos = range(len(desc_impacto))
ax2.bar(x_pos, desc_impacto["revenue_prom"],
        color=PALETTE["secondary"], alpha=0.7, label="Revenue promedio")
ax2_twin.plot(x_pos, desc_impacto["margen_prom"],
              color=PALETTE["accent"], marker="o", linewidth=2.5,
              markersize=8, label="Margen %")
ax2.set_xticks(list(x_pos))
ax2.set_xticklabels([f"{int(d*100)}%" for d in desc_impacto["descuento_pct"]])
ax2.set_xlabel("Descuento aplicado")
ax2.set_ylabel("Revenue promedio (RD$)")
ax2_twin.set_ylabel("Margen promedio (%)", color=PALETTE["accent"])
ax2.set_title("Revenue vs Margen por nivel de descuento",
              fontweight="bold", color=PALETTE["neutral"])

lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("../outputs/06_analisis_descuentos.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# ## 9. KPIs Ejecutivos — Resumen Final

# %%
# Crecimiento YoY
rev_2023 = ventas_limpias[ventas_limpias["año"] == 2023]["total_venta"].sum()
rev_2024 = ventas_limpias[ventas_limpias["año"] == 2024]["total_venta"].sum()
crecimiento = (rev_2024 - rev_2023) / rev_2023 * 100

mejor_categoria = cat_resumen.loc[cat_resumen["revenue"].idxmax(), "categoria"]
mejor_tienda    = tienda_resumen.loc[tienda_resumen["revenue"].idxmax(), "tienda_nombre"]
tasa_devolucion = df["devolucion"].mean() * 100

print("=" * 60)
print("           REPORTE EJECUTIVO FINAL")
print("=" * 60)
print(f"  Revenue 2023:          ${rev_2023:>14,.0f}")
print(f"  Revenue 2024:          ${rev_2024:>14,.0f}")
print(f"  Crecimiento YoY:       {crecimiento:>13.1f}%")
print(f"  Mejor categoría:       {mejor_categoria:>20}")
print(f"  Mejor tienda:          {mejor_tienda:>20}")
print(f"  Tasa de devolución:    {tasa_devolucion:>13.1f}%")
print(f"  Clientes Champions:    {len(rfm[rfm['Segmento']=='Champions']):>13,}")
print("=" * 60)
print("\n✅ Análisis completo. Gráficos guardados en /outputs/")
