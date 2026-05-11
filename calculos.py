def calcular_preco(

    custo_produto,
    frete,
    outros_custos,

    impostos,
    taxas,
    comissao,
    administrativo,
    perdas,

    margem

):

    # =====================================
    # CUSTOS DIRETOS
    # =====================================

    custos_diretos = (

        custo_produto +
        frete +
        outros_custos

    )

    # =====================================
    # CUSTOS PERCENTUAIS
    # =====================================

    percentual_operacional = (

        impostos +
        taxas +
        comissao +
        administrativo +
        perdas

    )

    # =====================================
    # PERCENTUAL TOTAL
    # =====================================

    percentual_total = (

        percentual_operacional +
        margem

    )

    percentual_decimal = percentual_total / 100

    # =====================================
    # VALIDAÇÃO
    # =====================================

    if percentual_decimal >= 1:

        return {

            "erro": "Os percentuais não podem somar 100% ou mais."

        }

    # =====================================
    # PREÇO SUGERIDO
    # =====================================

    preco_sugerido = (

        custos_diretos /

        (1 - percentual_decimal)

    )

    # =====================================
    # CÁLCULO DOS CUSTOS PERCENTUAIS
    # =====================================

    valor_impostos = (

        preco_sugerido *
        (impostos / 100)

    )

    valor_taxas = (

        preco_sugerido *
        (taxas / 100)

    )

    valor_comissao = (

        preco_sugerido *
        (comissao / 100)

    )

    valor_administrativo = (

        preco_sugerido *
        (administrativo / 100)

    )

    valor_perdas = (

        preco_sugerido *
        (perdas / 100)

    )

    # =====================================
    # LUCRO LÍQUIDO
    # =====================================

    lucro = (

        preco_sugerido

        - custos_diretos

        - valor_impostos
        - valor_taxas
        - valor_comissao
        - valor_administrativo
        - valor_perdas

    )

    # =====================================
    # MARGEM REAL
    # =====================================

    margem_real = (

        lucro / preco_sugerido

    ) * 100

    # =====================================
    # MARKUP EQUIVALENTE
    # =====================================

    markup = (

        preco_sugerido /

        custos_diretos

    )

    return {

        "custos_diretos": round(custos_diretos, 2),

        "preco_sugerido": round(preco_sugerido, 2),

        "lucro": round(lucro, 2),

        "margem_real": round(margem_real, 2),

        "markup": round(markup, 2),

        "valor_impostos": round(valor_impostos, 2),

        "valor_taxas": round(valor_taxas, 2),

        "valor_comissao": round(valor_comissao, 2),

        "valor_administrativo": round(valor_administrativo, 2),

        "valor_perdas": round(valor_perdas, 2),

        "percentual_operacional": round(percentual_operacional, 2),

        "percentual_total": round(percentual_total, 2)

    }