def calcular_preco(
    custo_produto,
    frete,
    outros_custos,
    impostos,
    taxas,
    comissao,
    margem
):

    # =========================
    # CUSTOS FIXOS
    # =========================
    custos_fixos = (
        custo_produto +
        frete +
        outros_custos
    )

    # =========================
    # SOMA DOS PERCENTUAIS
    # =========================
    percentual_total = (
        impostos +
        taxas +
        comissao +
        margem
    )

    # Converter para decimal
    percentual_decimal = percentual_total / 100

    # Evitar erro matemático
    if percentual_decimal >= 1:
        return {
            "erro": "Percentuais não podem somar 100% ou mais."
        }

    # =========================
    # CÁLCULO DO PREÇO
    # =========================
    preco_sugerido = custos_fixos / (1 - percentual_decimal)

    # =========================
    # CÁLCULO DO LUCRO
    # =========================
    lucro = preco_sugerido - custos_fixos

    return {
        "custos_fixos": round(custos_fixos, 2),
        "percentual_total": round(percentual_total, 2),
        "preco_sugerido": round(preco_sugerido, 2),
        "lucro": round(lucro, 2),
        "margem": margem
    }