
import tkinter as tk
from tkinter import ttk, messagebox

import servicos


class FitManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FitManager | Gestão de Academia")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        self.aluno_selecionado = None
        self.alunos_cache = []

        self.configurar_estilo()
        self.criar_interface()
        self.atualizar_tudo()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TNotebook",
            background="#f1f5f9",
            borderwidth=0
        )
        estilo.configure(
            "TNotebook.Tab",
            padding=(18, 10),
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white"
        )
        estilo.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold")
        )
        estilo.configure(
            "TButton",
            padding=8,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "TLabel",
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "TEntry",
            padding=6
        )

    def criar_interface(self):
        cabecalho = tk.Frame(self.root, bg="#14213d", height=100)
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        tk.Label(
            cabecalho,
            text="FitManager",
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#14213d"
        ).pack(anchor="w", padx=25, pady=(15, 0))

        tk.Label(
            cabecalho,
            text="Sistema de gestão de academia",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#14213d"
        ).pack(anchor="w", padx=27)

        self.abas = ttk.Notebook(self.root)
        self.abas.pack(fill="both", expand=True, padx=18, pady=18)

        self.aba_alunos = ttk.Frame(self.abas, padding=15)
        self.aba_pagamentos = ttk.Frame(self.abas, padding=15)
        self.aba_frequencia = ttk.Frame(self.abas, padding=15)

        self.abas.add(self.aba_alunos, text="Alunos")
        self.abas.add(self.aba_pagamentos, text="Pagamentos")
        self.abas.add(self.aba_frequencia, text="Frequência")

        self.criar_aba_alunos()
        self.criar_aba_pagamentos()
        self.criar_aba_frequencia()

        self.status = ttk.Label(
            self.root,
            text="FitManager conectado ao Supabase",
            anchor="w"
        )
        self.status.pack(fill="x", padx=20, pady=(0, 10))

    def criar_aba_alunos(self):
        ttk.Label(
            self.aba_alunos,
            text="Gerenciamento de alunos",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", pady=(0, 12))

        pesquisa = ttk.Frame(self.aba_alunos)
        pesquisa.pack(fill="x", pady=(0, 12))

        ttk.Label(pesquisa, text="Pesquisar por nome:").pack(
            side="left", padx=(0, 8)
        )

        self.campo_pesquisa = ttk.Entry(pesquisa)
        self.campo_pesquisa.pack(side="left", fill="x", expand=True)
        self.campo_pesquisa.bind(
            "<Return>",
            lambda event: self.carregar_alunos()
        )

        ttk.Button(
            pesquisa,
            text="Pesquisar",
            command=self.carregar_alunos
        ).pack(side="left", padx=6)

        ttk.Button(
            pesquisa,
            text="Mostrar todos",
            command=self.limpar_pesquisa
        ).pack(side="left")

        formulario = ttk.LabelFrame(
            self.aba_alunos,
            text="Dados do aluno",
            padding=12
        )
        formulario.pack(fill="x", pady=(0, 12))

        ttk.Label(formulario, text="Nome completo").grid(
            row=0, column=0, sticky="w", padx=5, pady=4
        )
        ttk.Label(formulario, text="Telefone").grid(
            row=0, column=1, sticky="w", padx=5, pady=4
        )
        ttk.Label(formulario, text="Plano").grid(
            row=0, column=2, sticky="w", padx=5, pady=4
        )
        ttk.Label(formulario, text="Pagamento").grid(
            row=0, column=3, sticky="w", padx=5, pady=4
        )

        self.campo_nome = ttk.Entry(formulario)
        self.campo_telefone = ttk.Entry(formulario)
        self.campo_plano = ttk.Combobox(
            formulario,
            values=["Mensal", "Trimestral", "Semestral", "Anual"],
            state="normal"
        )
        self.campo_pagamento = ttk.Combobox(
            formulario,
            values=["Em dia", "Pendente"],
            state="readonly"
        )
        self.campo_pagamento.set("Em dia")

        self.campo_nome.grid(
            row=1, column=0, sticky="ew", padx=5, pady=4
        )
        self.campo_telefone.grid(
            row=1, column=1, sticky="ew", padx=5, pady=4
        )
        self.campo_plano.grid(
            row=1, column=2, sticky="ew", padx=5, pady=4
        )
        self.campo_pagamento.grid(
            row=1, column=3, sticky="ew", padx=5, pady=4
        )

        for coluna in range(4):
            formulario.columnconfigure(coluna, weight=1)

        botoes = ttk.Frame(self.aba_alunos)
        botoes.pack(fill="x", pady=(0, 12))

        ttk.Button(
            botoes,
            text="Cadastrar aluno",
            command=self.cadastrar
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            botoes,
            text="Salvar edição",
            command=self.editar
        ).pack(side="left", padx=6)

        ttk.Button(
            botoes,
            text="Excluir aluno",
            command=self.excluir
        ).pack(side="left", padx=6)

        ttk.Button(
            botoes,
            text="Limpar formulário",
            command=self.limpar_formulario
        ).pack(side="left", padx=6)

        colunas = (
            "id", "nome", "telefone", "plano", "pagamento"
        )

        self.tabela_alunos = ttk.Treeview(
            self.aba_alunos,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        titulos = {
            "id": "ID",
            "nome": "Nome",
            "telefone": "Telefone",
            "plano": "Plano",
            "pagamento": "Pagamento"
        }

        larguras = {
            "id": 55,
            "nome": 260,
            "telefone": 150,
            "plano": 130,
            "pagamento": 130
        }

        for coluna in colunas:
            self.tabela_alunos.heading(
                coluna, text=titulos[coluna]
            )
            self.tabela_alunos.column(
                coluna,
                width=larguras[coluna],
                anchor="w"
            )

        self.tabela_alunos.pack(fill="both", expand=True)
        self.tabela_alunos.bind(
            "<<TreeviewSelect>>",
            self.selecionar_aluno
        )

    def criar_aba_pagamentos(self):
        ttk.Label(
            self.aba_pagamentos,
            text="Controle de pagamentos",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", pady=(0, 8))

        ttk.Label(
            self.aba_pagamentos,
            text="Selecione um aluno para alterar a situação da mensalidade."
        ).pack(anchor="w", pady=(0, 12))

        colunas = ("id", "nome", "plano", "pagamento")

        self.tabela_pagamentos = ttk.Treeview(
            self.aba_pagamentos,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        for coluna, titulo in [
            ("id", "ID"),
            ("nome", "Nome do aluno"),
            ("plano", "Plano"),
            ("pagamento", "Situação")
        ]:
            self.tabela_pagamentos.heading(
                coluna, text=titulo
            )

        self.tabela_pagamentos.column("id", width=60)
        self.tabela_pagamentos.column("nome", width=300)
        self.tabela_pagamentos.column("plano", width=180)
        self.tabela_pagamentos.column("pagamento", width=180)

        self.tabela_pagamentos.pack(
            fill="both", expand=True, pady=(0, 12)
        )

        ttk.Button(
            self.aba_pagamentos,
            text="Alternar situação do pagamento",
            command=self.alternar_pagamento
        ).pack(anchor="w")

    def criar_aba_frequencia(self):
        ttk.Label(
            self.aba_frequencia,
            text="Controle de frequência",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", pady=(0, 12))

        painel = ttk.LabelFrame(
            self.aba_frequencia,
            text="Registrar entrada",
            padding=12
        )
        painel.pack(fill="x", pady=(0, 15))

        ttk.Label(
            painel,
            text="Selecione o aluno:"
        ).pack(side="left", padx=(0, 8))

        self.selecao_aluno = ttk.Combobox(
            painel,
            state="readonly",
            width=45
        )
        self.selecao_aluno.pack(
            side="left", fill="x", expand=True, padx=5
        )

        ttk.Button(
            painel,
            text="Registrar frequência",
            command=self.registrar
        ).pack(side="left", padx=5)

        ttk.Label(
            self.aba_frequencia,
            text="Últimos 100 registros",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        colunas = ("id", "aluno", "data_hora")

        self.tabela_frequencia = ttk.Treeview(
            self.aba_frequencia,
            columns=colunas,
            show="headings"
        )

        self.tabela_frequencia.heading("id", text="ID")
        self.tabela_frequencia.heading(
            "aluno", text="Aluno"
        )
        self.tabela_frequencia.heading(
            "data_hora", text="Data e hora"
        )

        self.tabela_frequencia.column("id", width=70)
        self.tabela_frequencia.column("aluno", width=350)
        self.tabela_frequencia.column("data_hora", width=260)

        self.tabela_frequencia.pack(
            fill="both", expand=True
        )

    def atualizar_tudo(self):
        try:
            self.carregar_alunos()
            self.carregar_pagamentos()
            self.carregar_opcoes_alunos()
            self.carregar_frequencias()
            self.status.config(
                text="Conectado ao Supabase"
            )
        except Exception as erro:
            self.status.config(
                text="Não foi possível carregar os dados."
            )
            messagebox.showerror(
                "Erro ao carregar dados",
                str(erro)
            )

    def carregar_alunos(self):
        try:
            busca = self.campo_pesquisa.get()
            alunos = servicos.listar_alunos(busca)
            self.alunos_cache = servicos.listar_alunos()

            for item in self.tabela_alunos.get_children():
                self.tabela_alunos.delete(item)

            for aluno in alunos:
                self.tabela_alunos.insert(
                    "",
                    "end",
                    iid=str(aluno["id"]),
                    values=(
                        aluno["id"],
                        aluno["nome"],
                        aluno.get("telefone", ""),
                        aluno["plano"],
                        aluno["pagamento"]
                    )
                )

            self.carregar_opcoes_alunos()
        except Exception as erro:
            messagebox.showerror(
                "Erro",
                f"Não foi possível listar os alunos:\n{erro}"
            )

    def carregar_pagamentos(self):
        alunos = servicos.listar_alunos()

        for item in self.tabela_pagamentos.get_children():
            self.tabela_pagamentos.delete(item)

        for aluno in alunos:
            self.tabela_pagamentos.insert(
                "",
                "end",
                iid=str(aluno["id"]),
                values=(
                    aluno["id"],
                    aluno["nome"],
                    aluno["plano"],
                    aluno["pagamento"]
                )
            )

    def carregar_opcoes_alunos(self):
        self.alunos_cache = servicos.listar_alunos()

        self.mapa_alunos = {}

        for aluno in self.alunos_cache:
            rotulo = f'{aluno["id"]} - {aluno["nome"]}'
            self.mapa_alunos[rotulo] = aluno["id"]

        self.selecao_aluno["values"] = list(
            self.mapa_alunos.keys()
        )

        if self.selecao_aluno.get() not in self.mapa_alunos:
            self.selecao_aluno.set("")

    def carregar_frequencias(self):
        frequencias = servicos.listar_frequencias()

        nomes = {
            aluno["id"]: aluno["nome"]
            for aluno in servicos.listar_alunos()
        }

        for item in self.tabela_frequencia.get_children():
            self.tabela_frequencia.delete(item)

        for frequencia in frequencias:
            aluno_id = frequencia["aluno_id"]
            nome = nomes.get(aluno_id, "Aluno não encontrado")

            self.tabela_frequencia.insert(
                "",
                "end",
                values=(
                    frequencia["id"],
                    nome,
                    frequencia["data_hora"]
                )
            )

    def obter_dados_formulario(self):
        return (
            self.campo_nome.get(),
            self.campo_telefone.get(),
            self.campo_plano.get(),
            self.campo_pagamento.get()
        )

    def cadastrar(self):
        try:
            dados = self.obter_dados_formulario()

            servicos.cadastrar_aluno(*dados)

            messagebox.showinfo(
                "Sucesso",
                "Aluno cadastrado com sucesso!"
            )

            self.limpar_formulario()
            self.atualizar_tudo()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao cadastrar",
                str(erro)
            )

    def selecionar_aluno(self, evento=None):
        selecionados = self.tabela_alunos.selection()

        if not selecionados:
            return

        aluno_id = int(selecionados[0])

        aluno = next(
            (
                item for item in self.alunos_cache
                if item["id"] == aluno_id
            ),
            None
        )

        if aluno is None:
            return

        self.aluno_selecionado = aluno_id

        self.campo_nome.delete(0, tk.END)
        self.campo_nome.insert(0, aluno["nome"])

        self.campo_telefone.delete(0, tk.END)
        self.campo_telefone.insert(
            0, aluno.get("telefone", "")
        )

        self.campo_plano.set(aluno["plano"])
        self.campo_pagamento.set(aluno["pagamento"])

    def editar(self):
        if self.aluno_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno na tabela antes de editar."
            )
            return

        try:
            servicos.atualizar_aluno(
                self.aluno_selecionado,
                *self.obter_dados_formulario()
            )

            messagebox.showinfo(
                "Sucesso",
                "Cadastro atualizado com sucesso!"
            )

            self.limpar_formulario()
            self.atualizar_tudo()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao editar",
                str(erro)
            )

    def excluir(self):
        selecionados = self.tabela_alunos.selection()

        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno para excluir."
            )
            return

        aluno_id = int(selecionados[0])

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este aluno? "
            "As frequências vinculadas também serão excluídas."
        )

        if not confirmar:
            return

        try:
            servicos.excluir_aluno(aluno_id)

            messagebox.showinfo(
                "Sucesso",
                "Aluno excluído."
            )

            self.limpar_formulario()
            self.atualizar_tudo()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                str(erro)
            )

    def alternar_pagamento(self):
        selecionados = self.tabela_pagamentos.selection()

        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno na tabela de pagamentos."
            )
            return

        aluno_id = int(selecionados[0])

        aluno = next(
            (
                item for item in servicos.listar_alunos()
                if item["id"] == aluno_id
            ),
            None
        )

        if aluno is None:
            messagebox.showerror(
                "Erro",
                "Aluno não encontrado."
            )
            return

        novo_status = (
            "Pendente"
            if aluno["pagamento"] == "Em dia"
            else "Em dia"
        )

        try:
            servicos.atualizar_aluno(
                aluno_id,
                aluno["nome"],
                aluno.get("telefone", ""),
                aluno["plano"],
                novo_status
            )

            self.atualizar_tudo()

            messagebox.showinfo(
                "Pagamento atualizado",
                f'Situação alterada para "{novo_status}".'
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def registrar(self):
        rotulo = self.selecao_aluno.get()

        if rotulo not in self.mapa_alunos:
            messagebox.showwarning(
                "Atenção",
                "Selecione um aluno antes de registrar."
            )
            return

        aluno_id = self.mapa_alunos[rotulo]

        try:
            servicos.registrar_frequencia(aluno_id)

            messagebox.showinfo(
                "Sucesso",
                "Frequência registrada com sucesso!"
            )

            self.carregar_frequencias()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao registrar frequência",
                str(erro)
            )

    def limpar_pesquisa(self):
        self.campo_pesquisa.delete(0, tk.END)
        self.carregar_alunos()

    def limpar_formulario(self):
        self.aluno_selecionado = None

        self.campo_nome.delete(0, tk.END)
        self.campo_telefone.delete(0, tk.END)
        self.campo_plano.set("")
        self.campo_pagamento.set("Em dia")

        for item in self.tabela_alunos.selection():
            self.tabela_alunos.selection_remove(item)
