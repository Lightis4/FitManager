
from banco import supabase


def listar_alunos(busca=""):
    consulta = supabase.table("alunos").select("*")

    if busca.strip():
        consulta = consulta.ilike("nome", f"%{busca.strip()}%")

    resposta = consulta.order("nome").execute()
    return resposta.data


def cadastrar_aluno(nome, telefone, plano, pagamento):
    nome = nome.strip()
    plano = plano.strip()

    if not nome:
        raise ValueError("Informe o nome do aluno.")

    if not plano:
        raise ValueError("Informe o plano do aluno.")

    dados = {
        "nome": nome,
        "telefone": telefone.strip(),
        "plano": plano,
        "pagamento": pagamento
    }

    resposta = supabase.table("alunos").insert(dados).execute()
    return resposta.data


def atualizar_aluno(aluno_id, nome, telefone, plano, pagamento):
    nome = nome.strip()
    plano = plano.strip()

    if not nome:
        raise ValueError("Informe o nome do aluno.")

    if not plano:
        raise ValueError("Informe o plano do aluno.")

    dados = {
        "nome": nome,
        "telefone": telefone.strip(),
        "plano": plano,
        "pagamento": pagamento
    }

    resposta = (
        supabase.table("alunos")
        .update(dados)
        .eq("id", aluno_id)
        .execute()
    )

    return resposta.data


def excluir_aluno(aluno_id):
    resposta = (
        supabase.table("alunos")
        .delete()
        .eq("id", aluno_id)
        .execute()
    )

    return resposta.data


def registrar_frequencia(aluno_id):
    resposta = (
        supabase.table("frequencias")
        .insert({"aluno_id": int(aluno_id)})
        .execute()
    )

    return resposta.data


def listar_frequencias():
    resposta = (
        supabase.table("frequencias")
        .select("*")
        .order("data_hora", desc=True)
        .limit(100)
        .execute()
    )

    return resposta.data
