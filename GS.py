# =============================================================================
# FireWatch — Modelagem Matemática do Risco de Propagação de Queimadas
# =============================================================================
# Disciplina : Differentiated Problem Solving
# Instituição : FIAP — Engenharia de Software — 1º Ano — 2026
#
# Integrantes:
#   Fernando Lima    — RM: 570847
#   Enzo Gabriel     — RM: 571357
#   Cesar Duarte     — RM: 571357
#   Enzo Castilho    — RM: 570108
#   Wesley Ferreira  — RM: 573479
#
# -----------------------------------------------------------------------------
# DESCRIÇÃO DO MODELO MATEMÁTICO
# -----------------------------------------------------------------------------
# Função principal  : R(s) = e^(0,3 × s)
# Variável          : s = índice de seca regional (fonte: satélite Copernicus)
# Saída             : R = nível de risco de propagação calculado pelo FireWatch
#
# Domínio           : s ∈ [0, 10]
#                     0 → ausência total de seca
#                    10 → seca extrema
#
# Imagem            : R ∈ [1,00 ; 20,09]
#                     R(0)  = e^0   = 1,00  (risco mínimo)
#                     R(10) = e^3  ≈ 20,09  (risco máximo)
#
# Derivada          : R'(s) = 0,3 × e^(0,3s)
#                     Sempre positiva → função estritamente crescente
#                     Taxa de crescimento aumenta com s (comportamento exponencial)
#
# Limiares de risco:
#   Controlado  → R < 4,00   (s < ~4,6)
#   Moderado    → 4,00 ≤ R < 7,00   (4,6 ≤ s < ~6,5)
#   Crítico     → R ≥ 7,00   (s ≥ ~6,5)
# =============================================================================

# =============================================================================
# PARTE 1 — CABEÇALHO E COMENTÁRIOS
# (descrição completa do modelo acima)
# =============================================================================

# =============================================================================
# PARTE 2 — IMPORTAÇÕES
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# =============================================================================
# PARTE 3 — DEFINIÇÃO DA FUNÇÃO
# =============================================================================

def risco_propagacao(s):
    """
    Calcula o nível de risco de propagação de queimadas.

    Parâmetro:
        s (float): índice de seca regional no intervalo [0, 10]

    Retorna:
        float: nível de risco R = e^(0,3 × s)
    """
    return np.exp(0.3 * s)


def classificar_risco(r):
    """
    Classifica o nível de risco em três categorias do FireWatch.

    Parâmetro:
        r (float): valor de risco calculado por risco_propagacao(s)

    Retorna:
        str: 'CONTROLADO', 'MODERADO' ou 'CRÍTICO'
    """
    if r < 4.0:
        return "CONTROLADO"
    elif r < 7.0:
        return "MODERADO"
    else:
        return "CRÍTICO"


# =============================================================================
# PARTE 4 — GERAÇÃO DOS DADOS PARA O GRÁFICO
# =============================================================================

# 100 pontos igualmente espaçados no domínio [0, 10]
s_valores = np.linspace(0, 10, 100)
r_valores  = risco_propagacao(s_valores)

# Limiares de risco (valor de R correspondente a cada fronteira)
LIMIAR_MODERADO = 4.0   # R >= 4  → zona moderada
LIMIAR_CRITICO  = 7.0   # R >= 7  → zona crítica

# Índice de seca correspondente a cada limiar (invertendo a função)
# s = ln(R) / 0,3
s_limiar_moderado = np.log(LIMIAR_MODERADO) / 0.3   # ≈ 4,62
s_limiar_critico  = np.log(LIMIAR_CRITICO)  / 0.3   # ≈ 6,49


# =============================================================================
# PARTE 5 — PONTOS DAS REGIÕES AMAZÔNICAS MONITORADAS
# =============================================================================

regioes = {
    "Sul do Pará":            9.1,
    "Norte de Mato Grosso":   8.5,
    "Sul de Rondônia":        7.8,
    "Sudoeste do Amazonas":   6.2,
}




# =============================================================================
# PARTE 6 — CONSTRUÇÃO DO GRÁFICO
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor("#0d0d0d")
ax.set_facecolor("#0d0d0d")

# --- Zonas coloridas de risco ---
ax.fill_between(s_valores, r_valores,
                where=(s_valores <= s_limiar_moderado),
                color="#1a4a2e", alpha=0.5, label="Zona Controlada")

ax.fill_between(s_valores, r_valores,
                where=((s_valores > s_limiar_moderado) & (s_valores <= s_limiar_critico)),
                color="#7a5c00", alpha=0.5, label="Zona Moderada")

ax.fill_between(s_valores, r_valores,
                where=(s_valores > s_limiar_critico),
                color="#6b1a1a", alpha=0.5, label="Zona Crítica")

# --- Curva principal ---
ax.plot(s_valores, r_valores, color="#ff6b35", linewidth=2.5,
        label=r"$R(s) = e^{0{,}3s}$", zorder=5)

# --- Linhas de limiar ---
ax.axhline(y=LIMIAR_MODERADO, color="#f0c040", linestyle="--",
        linewidth=1.2, alpha=0.8, label=f"Limiar Moderado (R = {LIMIAR_MODERADO})")
ax.axhline(y=LIMIAR_CRITICO,  color="#e05050", linestyle="--",
        linewidth=1.2, alpha=0.8, label=f"Limiar Crítico (R = {LIMIAR_CRITICO})")

# --- Pontos das regiões amazônicas ---
cores_pontos = ["#e05050", "#e05050", "#e07030", "#f0c040"]
for i, (nome, s_val) in enumerate(regioes.items()):
    r_val = risco_propagacao(s_val)
    ax.scatter(s_val, r_val, color=cores_pontos[i], s=90, zorder=10,
            edgecolors="white", linewidths=0.8)
    ax.annotate(
        nome,
        xy=(s_val, r_val),
        xytext=(s_val - 2.8, r_val + 0.5),
        fontsize=8,
        color="white",
        arrowprops=dict(arrowstyle="->", color="gray", lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="#1e1e1e", ec="gray", lw=0.6)
    )

# --- Formatação dos eixos e título ---
ax.set_title(
    "FireWatch — Risco de Propagação de Queimadas\n"
    r"$R(s) = e^{0{,}3s}$  |  Regiões Amazônicas Monitoradas",
    fontsize=14, color="white", pad=15, fontweight="bold"
)
ax.set_xlabel("Índice de Seca Regional (s) — Fonte: Copernicus",
            fontsize=11, color="#cccccc")
ax.set_ylabel("Nível de Risco de Propagação R(s)",
            fontsize=11, color="#cccccc")

ax.set_xlim(0, 10)
ax.set_ylim(0, 22)
ax.set_xticks(range(0, 11))
ax.set_yticks(range(0, 23, 2))

ax.tick_params(colors="white", labelsize=9)
for spine in ax.spines.values():
    spine.set_edgecolor("#444444")

ax.grid(color="#333333", linestyle="--", linewidth=0.6, alpha=0.7)

# --- Legenda ---
patch_ctrl = mpatches.Patch(color="#1a4a2e", alpha=0.8, label="Controlado  (R < 4)")
patch_mod  = mpatches.Patch(color="#7a5c00", alpha=0.8, label="Moderado  (4 ≤ R < 7)")
patch_crit = mpatches.Patch(color="#6b1a1a", alpha=0.8, label="Crítico  (R ≥ 7)")
linha_curva = plt.Line2D([0], [0], color="#ff6b35", linewidth=2,
                        label=r"$R(s) = e^{0{,}3s}$")

ax.legend(
    handles=[linha_curva, patch_ctrl, patch_mod, patch_crit],
    loc="upper left", fontsize=9,
    facecolor="#1e1e1e", edgecolor="#555555", labelcolor="white"
)

plt.tight_layout()

# =============================================================================
# PARTE 7 — SALVAR E EXIBIR
# =============================================================================

# --- Salvar e exibir ---
nome_arquivo = "firewatch_risco_propagacao.png"
plt.savefig(nome_arquivo, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"\n✅ Gráfico salvo como '{nome_arquivo}'\n")
plt.show()


# =============================================================================
# PARTE 8 — TABELA NUMÉRICA NO TERMINAL
# =============================================================================

print("=" * 60)
print("  FireWatch — Tabela de Risco de Propagação")
print("  R(s) = e^(0,3 × s)   |   Domínio: s ∈ [0, 10]")
print("=" * 60)
print(f"  {'s':>4}   {'R(s)':>8}   {'Nível':<12}")
print("-" * 40)

for s in range(0, 11):
    r = risco_propagacao(s)
    nivel = classificar_risco(r)
    print(f"  {s:>4}   {r:>8.2f}   {nivel:<12}")

print("=" * 60)


# =============================================================================
# PARTE 9 — ANÁLISE MATEMÁTICA IMPRESSA NO TERMINAL
# =============================================================================

print("\n" + "=" * 60)
print("  Análise Matemática — FireWatch")
print("=" * 60)

print(f"""
Função       : R(s) = e^(0,3 × s)
Domínio      : s ∈ [0, 10]
Imagem       : R ∈ [{risco_propagacao(0):.2f} ; {risco_propagacao(10):.2f}]

Derivada     : R'(s) = 0,3 × e^(0,3s)
Comportamento: Estritamente crescente em todo o domínio
                (R'(s) > 0 para todo s)

Limiares:
    Controlado  → R < {LIMIAR_MODERADO:.1f}   (s < {s_limiar_moderado:.2f})
    Moderado    → {LIMIAR_MODERADO:.1f} ≤ R < {LIMIAR_CRITICO:.1f}  ({s_limiar_moderado:.2f} ≤ s < {s_limiar_critico:.2f})
    Crítico     → R ≥ {LIMIAR_CRITICO:.1f}   (s ≥ {s_limiar_critico:.2f})
""")

print("  Regiões Amazônicas Monitoradas:")
print(f"  {'Região':<28}  {'s':>5}  {'R(s)':>8}  {'Nível'}")
print("  " + "-" * 55)
for nome, s_val in regioes.items():
    r_val = risco_propagacao(s_val)
    nivel = classificar_risco(r_val)
    print(f"  {nome:<28}  {s_val:>5.1f}  {r_val:>8.2f}  {nivel}")

print("\n" + "=" * 60)
print("  FireWatch — FIAP Engenharia de Software 2026")
print("=" * 60 + "\n")