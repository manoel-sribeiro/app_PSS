import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import plotly.graph_objects as go
from scipy.spatial import ConvexHull
import folium
from streamlit_folium import st_folium
from PIL import Image
import time
from datetime import datetime
import os
from io import BytesIO
import random

# Menu na barra lateral
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Home", "Registro de Resíduos Triados", "Registro  - Troca de Resíduo por Alimento", "Visualização de Dados","Ranking da Reciclagem", "Compra e Venda de Material" , "Educacional"])

if 'first_run' not in st.session_state:
    st.session_state.first_run = True  # Define como True no primeiro carregamento
    #st.write("Este é o primeiro carregamento!")
else:
    st.session_state.first_run = False  # Se já foi carregado, define como False
    #st.write("Este não é o primeiro carregamento.")

with tab1:
    image_url = "https://segredosdomundo.r7.com/wp-content/uploads/2020/08/como-reciclar-aprenda-a-recuperar-materiais-que-iriam-para-o-lixo.jpg"
    st.image(image_url)
    st.title('Observatório de Dados de Resíduos Sólidos')
    st.write('''
    Bem-vindo ao Observatório de Dados de Resíduos Sólidos!
    
    Este é um projeto de um sistema de gestão de resíduos sólidos desenvolvido pela Universidade Federal do Rio Grande do Sul.
     
    O projeto tem por objetivo incentivar a coleta seletiva, contribuir para a melhoria da gestão nas cooperativas de triagem de resíduos sólidos, garantir a rastreabilidade dos resíduos e aproximar os elos da cadeia.
    ''')
    st.write('''
    Acesse as outras abas para utilizar o sistema.
    
    Dê um play no vídeo abaixo, e entre no clima da reciclagem! Vamos juntos fazer a diferença!
    ''')
    st.video("https://www.youtube.com/watch?v=4OVW4SRYRp0")
    
    st.subheader("Onde Posso Entregar Meus Resíduos?")
    
    # Dados das cooperativas
    cooperativas = [
        {
            "nome": "COOPERTUCA - Cooperativa Campo da Tuca",
            "endereco": "Rua D, nº 200, Vila João Pessoa, CEP 91510-480",
            "telefone": "(51) 3227-1234",  # exemplo fictício
            "coordenadas": [-30.039298, -51.206624],
            "imagem": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-cK-6cshkkO6iwwfWm1tnJsqwuJOZdleVRQ&s"  # Exemplo de imagem
        },
        {
            "nome": "UTC Lomba do Pinheiro",
            "endereco": "Estrada Afonso Lourenço Mariante, nº 4401, Lomba do Pinheiro, CEP 91787-260",
            "telefone": "(51) 3267-5678",  # exemplo fictício
            "coordenadas": [-30.100907, -51.149224],
            "imagem": "https://st2.depositphotos.com/1829203/5555/v/450/depositphotos_55558095-stock-illustration-metal-recycling-cycle-illustration.jpg"  # Exemplo de imagem
        },
        {
            "nome": "Centro de Triagem da Vila Pinto",
            "endereco": "Rua T, nº 143, Bom Jesus, CEP 91420-300",
            "telefone": "(51) 3245-7890",  # exemplo fictício
            "coordenadas": [-30.035469, -51.207199],
            "imagem": "https://prefeitura.poa.br/sites/default/files/styles/horizontal_grande/http/bancodeimagens.portoalegre.rs.gov.br/sites/default/files/2021/05/18/20210518085542_AP2A3252.jpg?itok=JqDtOJ6I"  # Exemplo de imagem
        }
    ]

    # Título da aplicação
    #st.title("Mapa de Cooperativas de Triagem de Lixo - Porto Alegre")

    # Criar o mapa
    mapa = folium.Map(location=[-30.0346, -51.2177], zoom_start=12)

    # Adicionar marcadores ao mapa com ícones personalizados
    for coop in cooperativas:
        folium.Marker(
            location=coop["coordenadas"],
            popup=f"<b>{coop['nome']}</b><br>{coop['endereco']}<br>Telefone: {coop['telefone']}",
            tooltip=coop["nome"],
            icon=folium.Icon(color="green", icon="leaf", prefix="fa")  # Ícone verde com tema de sustentabilidade
        ).add_to(mapa)

    # Exibir o mapa no Streamlit
    st_folium(mapa, width=700)

    # Exibir lista com imagens abaixo do mapa
    st.subheader("Lista de Cooperativas")
    for coop in cooperativas:
        st.markdown(f"### {coop['nome']}")
        st.image(coop["imagem"], width=200)
        st.markdown(f"**Endereço:** {coop['endereco']}")
        st.markdown(f"**Telefone:** {coop['telefone']}")
        st.markdown("---")
    
    st.subheader("É responsável por uma cooperativa e deseja fazer parte do projeto?")
    st.write("Entre em contato conosco pelo e-mail: HelicePower@helicepowerufrgs.br")
    
with tab2:
    st.image("https://legislacaoemercados.capitalaberto.com.br/wp-content/uploads/2023/11/29.11_materia3.webp", caption="")
    st.title('Registro de Resíduos Triados')
    nome_cooperativa = st.selectbox("Nome da Cooperativa", ["COOPERTUCA - Cooperativa Campo da Tuca", "UTC Lomba do Pinheiro", "Centro de Triagem da Vila Pinto"])
    password = st.text_input("Digite a senha recebida", type="password")
    if password == "HelicePower":
        st.write("Acesso permitido!")
        with st.form(key="Resíduos Triados", clear_on_submit= True):
            Data_reg = st.date_input("Data")
            Origem_carga = st.text_input("Origem da Carga")
            Responsavel = st.text_input("Responsável")
            #Subheader
            st.markdown("**Amostra**")
            peso_bag1 = st.number_input("Peso da Bag 1 vazia (kg)", min_value=0.0, step=0.1, format="%f")
            peso_total_bag1 = st.number_input("Peso da Bag 1 com resíduos (kg)", min_value=0.0, step=0.1, format="%f")
            peso_bag2 = st.number_input("Peso da Bag 2 vazia (kg)", min_value=0.0, step=0.1, format="%f")
            peso_total_bag2 = st.number_input("Peso da Bag 2 com resíduos (kg)", min_value=0.0, step=0.1, format="%f")
            
            with st.expander("Plástico"):
                peso_plastico_total = st.number_input("Peso total de plástico (kg)", min_value=0.0, step=0.1, format="%f")
                pet_resina = st.number_input("PET Resina (kg)", min_value=0.0, step=0.1, format="%f")
                pet_transparente = st.number_input("PET Transparente (kg)", min_value=0.0, step=0.1, format="%f")
                pet_verde = st.number_input("PET Verde (kg)", min_value=0.0, step=0.1, format="%f")
                pebd_transparente = st.number_input("PEBD Transparente (kg)", min_value=0.0, step=0.1, format="%f")
                pebd_colorido = st.number_input("PEBD Colorido (kg)", min_value=0.0, step=0.1, format="%f")
                pead_brancos = st.number_input("PEAD Branco (kg)", min_value=0.0, step=0.1, format="%f")
                pead_coloridos = st.number_input("PEAD Colorido (kg)", min_value=0.0, step=0.1, format="%f")
                demais_plasticos = st.number_input("Demais Plásticos Triados (kg)", min_value=0.0, step=0.1, format="%f")
                comentarios_plastico = st.text_area("Comentários")
            
            with st.expander("Rejeitos"):
                peso_bag_bombona1 = st.number_input("Peso da Bag/Bombona 1 (kg)", min_value=0.0, step=0.1, format="%f")
                peso_bag_bombona2 = st.number_input("Peso da Bag/Bombona 2 (kg)", min_value=0.0, step=0.1, format="%f")
                peso_total_bag_bombona1 = st.number_input("Peso Total da Bag/Bombona 1 com Rejeito (kg)", min_value=0.0, step=0.1, format="%f")
                peso_total_bag_bombona2 = st.number_input("Peso Total da Bag/Bombona 2 com Rejeito (kg)", min_value=0.0, step=0.1, format="%f")
                rejeito_org = st.number_input("Rejeito Orgânico (kg)", min_value=0.0, step=0.1, format="%f")
                rejeito_diversos = st.number_input("Rejeito Diversos (kg)", min_value=0.0, step=0.1, format="%f")
                rejeito_papel = st.number_input("Rejeito Papel (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_papel = st.selectbox("Motivo do Rejeito de Papel", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Outro"])
                rejeito_vidro = st.number_input("Rejeito Vidro (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_vidro = st.selectbox("Motivo do Rejeito de Vidro", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Outro"])
                rejeito_metal = st.number_input("Rejeito Metal (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_metal = st.selectbox("Motivo do Rejeito de Metal", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Outro"])
                rejeito_plastico = st.number_input("Rejeito Plástico (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico = st.selectbox("Motivo do Rejeito de Plástico", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Outro"])
                rejeito_varredura = st.number_input("Rejeito Varredura (kg)", min_value=0.0, step=0.1, format="%f")
                rejeito_plastico_pet = st.number_input("Rejeito Plástico PET (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico_pet = st.selectbox("Motivo do Rejeito de Plástico PET", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                rejeito_plastico_pead = st.number_input("Rejeito Plástico PEAD (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico_pead = st.selectbox("Motivo do Rejeito de Plástico PEAD", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                rejeito_plastico_ps = st.number_input("Rejeito Plástico PS (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico_ps = st.selectbox("Motivo do Rejeito de Plástico PS", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                rejeito_plastico_pvc = st.number_input("Rejeito Plástico PVC (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico_pvc = st.selectbox("Motivo do Rejeito de Plástico PVC", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                rejeito_plastico_pp = st.number_input("Rejeito Plástico PP (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_plastico_pp = st.selectbox("Motivo do Rejeito de Plástico PP", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                rejeito_outros_plasticos = st.number_input("Rejeito Outros Plásticos (kg)", min_value=0.0, step=0.1, format="%f")
                motivo_rejeito_outros_plasticos = st.selectbox("Motivo do Rejeito de Outros Plásticos", ["Muito Pequeno", "Contaminado", "Não tem valor de mercado", "Não é possível separar o material", "Material não identificado","Laminação com plásticos diferentes","Plásticos de Engenharia que não se enquadram em commodities","Muito leve", "ineficiente para separação"])
                
                # Upload de múltiplas imagens
                uploaded_files = st.file_uploader(
                    "Escolha suas imagens para upload:", 
                    type=["png", "jpg", "jpeg"], 
                    accept_multiple_files=True
                )

                
                
            submited = st.form_submit_button("Salvar")
            if submited:
                dft = pd.DataFrame()
                dados = {
                    "Data": [Data_reg],
                    "Origem da Carga": [Origem_carga],
                    "Responsável": [Responsavel],
                    "Peso da Bag 1 vazia": [peso_bag1],
                    "Peso da Bag 1 com resíduos": [peso_total_bag1],
                    "Peso da Bag 2 vazia": [peso_bag2],
                    "Peso da Bag 2 com resíduos": [peso_total_bag2],
                    "Peso Total de Plástico": [peso_plastico_total],
                    "PET Resina": [pet_resina],
                    "PET Transparente": [pet_transparente],
                    "PET Verde": [pet_verde],
                    "PEBD Transparente": [pebd_transparente],
                    "PEBD Colorido": [pebd_colorido],
                    "PEAD Branco": [pead_brancos],
                    "PEAD Colorido": [pead_coloridos],
                    "Demais Plásticos Triados": [demais_plasticos],
                    "Comentários Plástico": [comentarios_plastico],
                    "Peso da Bag/Bombona 1": [peso_bag_bombona1],
                    "Peso da Bag/Bombona 2": [peso_bag_bombona2],
                    "Peso Total da Bag/Bombona 1 com Rejeito": [peso_total_bag_bombona1],
                    "Peso Total da Bag/Bombona 2 com Rejeito": [peso_total_bag_bombona2],
                    "Rejeito Orgânico": [rejeito_org],
                    "Rejeito Diversos": [rejeito_diversos],
                    "Rejeito Papel": [rejeito_papel],
                    "Motivo do Rejeito de Papel": [motivo_rejeito_papel],
                    "Rejeito Vidro": [rejeito_vidro],
                    "Motivo do Rejeito de Vidro": [motivo_rejeito_vidro],
                    "Rejeito Metal": [rejeito_metal],
                    "Motivo do Rejeito de Metal": [motivo_rejeito_metal],
                    "Rejeito Plástico": [rejeito_plastico],
                    "Motivo do Rejeito de Plástico": [motivo_rejeito_plastico],
                    "Rejeito Varredura": [rejeito_varredura]
                    
                }
                dft = pd.DataFrame(dados)
                
                dft.to_csv("residuos_triados.csv", mode="a", header=False, index=False, encoding="utf-8")
                
                # Processar e salvar as imagens enviadas
                if uploaded_files:
                    st.write(f"{len(uploaded_files)} imagens carregadas.")
                    for file in uploaded_files:
                        # Obter o tipo de arquivo e criar o nome do arquivo
                        extension = file.name.split(".")[-1]  # Extrair extensão
                        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Data e hora
                        filename = f"nome_{current_time}.{extension}"  # Nome personalizado

                        # Salvar o arquivo no diretório
                        file_path = os.path.join(filename)
                        with open(file_path, "wb") as f:
                            f.write(file.read())

                        # # Exibir mensagem de sucesso e visualização da imagem
                        # st.success(f"Imagem salva como: {filename}")
                        # image = Image.open(file_path)
                        # st.image(image, caption=f"Visualização: {filename}", use_column_width=True)
                else:
                    st.write("Nenhuma imagem enviada ainda.")
                st.write("Informações salvas!")
with tab3:
    st.image("troca de resíduo.png", caption="")
    st.title('Projeto Troca de Resíduo por Alimento')
    with st.expander("Novo cadastro de participante"):
        # Formulário de entrada
        st.header("Formulário de Cadastro")
        # Inicializar as variáveis no session_state, se não existirem
        
        def cria_forms():
            st.session_state.nome = st.text_input("Primeiro Nome", st.session_state.nome)
            st.session_state.sobrenome = st.text_input("Sobrenome", st.session_state.sobrenome)
            st.session_state.whatsapp = st.text_input("Whatsapp", st.session_state.whatsapp)
            st.session_state.endereço = st.text_input("Endereço", st.session_state.endereço)
            st.session_state.tipo_residencia = st.selectbox("Tipo de Estabelecimento", ["Casa", "Apartamento", "Comércio", "Outro"], index=["Casa", "Apartamento", "Comércio", "Outro"].index(st.session_state.tipo_residencia))
            if st.session_state.tipo_residencia == "Outro":
                st.session_state.tipo_residencia = st.text_input("Especificar outro tipo de estabelecimento", st.session_state.tipo_residencia)
            st.session_state.area_atuacao_CEA = st.selectbox("Área de Atuação do CEA", ["SASE (SCFV)", "PROJOVEM", "VOVÓ BELINHA (Funcionário)", "VOVÓ BELINHA (Pais)", "TRIADOR", "COMUNIDADE EM GERAL", "Outro"], index=["SASE (SCFV)", "PROJOVEM", "VOVÓ BELINHA (Funcionário)", "VOVÓ BELINHA (Pais)", "TRIADOR", "COMUNIDADE EM GERAL", "Outro"].index(st.session_state.area_atuacao_CEA))
            if st.session_state.area_atuacao_CEA == "Outro":
                st.session_state.area_atuacao_CEA = st.text_input("Especificar outra área de atuação", st.session_state.area_atuacao_CEA)
            if "VOVÓ BELINHA" in st.session_state.area_atuacao_CEA:
                st.session_state.nome_crianças = st.text_input("Nome da(s) criança(s)", st.session_state.nome_crianças)
            st.session_state.total_moradores = st.number_input("Total de moradores", min_value=1, step=1, format="%d", value=st.session_state.total_moradores)
            st.session_state.indicação = st.selectbox("O Participante foi indicado?", ["Sim", "Não"], index=["Sim", "Não"].index(st.session_state.indicação))
            if st.session_state.indicação == "Sim":
                st.session_state.indicador = st.text_input("Nome do indicador", st.session_state.indicador)
        
        if "sobrenome" not in st.session_state:
            st.session_state.sobrenome = ""
        if "whatsapp" not in st.session_state:
            st.session_state.whatsapp = ""
        if "endereço" not in st.session_state:
            st.session_state.endereço = ""
        if "tipo_residencia" not in st.session_state:
            st.session_state.tipo_residencia = "Casa"
        if "area_atuacao_CEA" not in st.session_state:
            st.session_state.area_atuacao_CEA = "SASE (SCFV)"
        if "nome_crianças" not in st.session_state:
            st.session_state.nome_crianças = ""
        if "total_moradores" not in st.session_state:
            st.session_state.total_moradores = 1
        if "indicação" not in st.session_state:
            st.session_state.indicação = "Não"
        if "indicador" not in st.session_state:
            st.session_state.indicador = ""
        if "nome" not in st.session_state:
            st.session_state.nome = ""
        
        

        # Função para limpar o formulário
        def limpar_formulario():
            st.session_state.nome = ""
            st.session_state.sobrenome = ""
            st.session_state.whatsapp = ""
            st.session_state.endereço = ""
            st.session_state.tipo_residencia = "Casa"
            st.session_state.area_atuacao_CEA = "SASE (SCFV)"
            st.session_state.nome_crianças = ""
            st.session_state.total_moradores = 1
            st.session_state.indicação = "Não"
            st.session_state.indicador = ""
           
        cria_forms()

        # Botão para salvar os dados
        if st.button("Salvar"):
            st.write("Informações salvas!")
            st.write(f"Nome: {st.session_state.nome}")
            st.write(f"Sobrenome: {st.session_state.sobrenome}")
            st.write(f"Whatsapp: {st.session_state.whatsapp}")
            st.write(f"Endereço: {st.session_state.endereço}")
            st.write(f"Tipo de Estabelecimento: {st.session_state.tipo_residencia}")
            st.write(f"Área de Atuação do CEA: {st.session_state.area_atuacao_CEA}")
            if "VOVÓ BELINHA" in st.session_state.area_atuacao_CEA:
                st.write(f"Nome da(s) criança(s): {st.session_state.nome_crianças}")
            st.write(f"Total de moradores: {st.session_state.total_moradores}")
            st.write(f"O Participante foi indicado? {st.session_state.indicação}")
            if st.session_state.indicação == "Sim":
                st.write(f"Nome do Indicador: {st.session_state.indicador}")
            
            df = pd.DataFrame()
                
            #Cria um DataFrame com as informações do formulário
            dados = {
                "Nome": [st.session_state.nome],
                "Sobrenome": [st.session_state.sobrenome],
                "Whatsapp": [st.session_state.whatsapp],
                "Endereço": [st.session_state.endereço],
                "Tipo de Estabelecimento": [st.session_state.tipo_residencia],
                "Área de Atuação do CEA": [st.session_state.area_atuacao_CEA],
                "Nome da(s) criança(s)": [st.session_state.nome_crianças],
                "Total de moradores": [st.session_state.total_moradores],
                "Indicação": [st.session_state.indicação],
                "Nome do Indicador": [st.session_state.indicador]
            }
            df = pd.DataFrame(dados)
            
            #salva o dataframe em um arquivo csv
            df.to_csv("participantes_troca_residuos.csv", mode="a", header=False, index=False, encoding="utf-8")
            limpar_formulario()
            st.rerun()
            
                
        # Botão para limpar o formulário
        if st.button("Limpar Formulário"):
            limpar_formulario()
            st.rerun()
                    
    with st.expander("Recebimento de resíduo"):
        with st.form(key="residuo-trocado", clear_on_submit=True):
            peso = 0.0
            df = pd.read_csv("participantes_troca_residuos.csv")
            Participante = st.selectbox("Nome do participante", df["Nome"] + " " + df["Sobrenome"])
            peso = st.number_input("PESO DO RESÍDUO SECO (kg)", min_value=0.0, step=0.1, format="%f", value = peso)
            data = st.date_input("Data")
            
            submited = st.form_submit_button("Salvar")
            if submited:
                dfr = pd.DataFrame()
                dados = {
                    "Nome": [Participante],
                    "Peso do Resíduo Seco": [peso],
                    "Data": [data]
                }
                dfr = pd.DataFrame(dados)
                
                dfr.to_csv("residuos_trocados.csv", mode="a", header=False,index=False, encoding="utf-8")
                st.write("Informações salvas!")
            
    with st.expander("Entrega de alimento"):
        with st.form(key="entrega-alimento", clear_on_submit=True):
            #inicializa as variáveis
            QTD_Açucar = 0.0
            QTD_LeitePo = 0.0
            Agua = 0.0
            Manta = 0
            
            Participante = st.selectbox("Nome do participante", df["Nome"] + " " + df["Sobrenome"], key="entrega-alimento")
            QTD_Açucar = st.number_input("Açúcar (kg)", min_value=0.0, step=0.1, format="%f", value = QTD_Açucar)
            QTD_LeitePo = st.number_input("Leite em Pó (kg)", min_value=0.0, step=0.1, format="%f", value = QTD_LeitePo)
            Agua = st.number_input("Água (L)", min_value=0.0, step=0.1, format="%f",    value = Agua)
            Manta = st.number_input("Manta", min_value=0, step=1, format="%d",  value = Manta)
            
            submited = st.form_submit_button("Salvar")
            if submited:
                dfa = pd.DataFrame()
                dados = {
                    "Nome": [Participante],
                    "Açúcar": [QTD_Açucar],
                    "Leite em Pó": [QTD_LeitePo],
                    "Água": [Agua],
                    "Manta": [Manta]
                }
                dfa = pd.DataFrame(dados)
                
                dfa.to_csv("alimentos_entregues.csv", mode="a", header=False,index=False, encoding="utf-8")
                st.write("Informações salvas!")
        
    with st.expander("Registro de resíduo final do turno"):
        with st.form(key= "residuo-final", clear_on_submit=True):
            #inicializa as variáveis
            peso_rejeito = 0.0
            peso_plastico = 0.0
            peso_papel_papelao = 0.0
            peso_aluminio_metal = 0.0
            peso_vidro = 0.0
            peso_sacolinha = 0.0
            peso_outros = 0.0
            data = st.date_input("Data", key="residuo-final")
            peso_rejeito = st.number_input("PESO DO REJEITO (kg)", min_value=0.0, step=0.1, format="%f", value = peso_rejeito)
            peso_plastico = st.number_input("PESO DO PLÁSTICO (kg)", min_value=0.0, step=0.1, format="%f", value = peso_plastico)
            peso_papel_papelao = st.number_input("PESO DO PAPEL/PAPLÃO (kg)", min_value=0.0, step=0.1, format="%f", value = peso_papel_papelao)
            peso_aluminio_metal = st.number_input("PESO DO ALUMÍNIO/METAL (kg)", min_value=0.0, step=0.1, format="%f", value = peso_aluminio_metal)
            peso_vidro = st.number_input("PESO DO VIDRO (kg)", min_value=0.0, step=0.1, format="%f", value = peso_vidro)
            peso_sacolinha = st.number_input("PESO DA SACOLINHA (kg)", min_value=0.0, step=0.1, format="%f", value = peso_sacolinha)
            peso_outros = st.number_input("PESO DE OUTROS MATERIAIS (kg)", min_value=0.0, step=0.1, format="%f", value = peso_outros)
                # Permitir que o usuário faça o upload de uma imagem
            uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "png", "jpeg"])

            # Verificar se o usuário fez upload de uma imagem
            if uploaded_file is not None:
                # Abrir a imagem com o Pillow (PIL)
                img = Image.open(uploaded_file)
                
                # Exibir a imagem no Streamlit
                #st.image(img, caption="Imagem carregada.")
                file_name, file_extension = os.path.splitext(uploaded_file.name)
                
            st.write("Informações salvas!")
            
            submited = st.form_submit_button("Salvar")
            if submited:
                dfrt = pd.DataFrame()
                dados = {
                    "Data": [data],
                    "Peso do Rejeito Final": [peso_rejeito],
                    "Peso do Plástico Final": [peso_plastico],
                    "Peso do Papel/Papelão Final": [peso_papel_papelao],
                    "Peso do Alumínio/Metal Final": [peso_aluminio_metal],
                    "Peso do Vidro Final": [peso_vidro],
                    "Peso da Sacolinha Final": [peso_sacolinha],
                    "Peso de Outros Materiais Final": [peso_outros]
                }
                dfrt = pd.DataFrame(dados)
                
                dfrt.to_csv("residuo_final_turno.csv", mode="a", header=False,index=False, encoding="utf-8")
                # Gera um nome de arquivo único com base na data e hora atual
                unique_filename = f"imagem_{int(time.time())}.{file_extension}"
                img.save(unique_filename)    
            
            
                
    with st.expander("Fidelidade"):
        # A senha vem do arquivo secrets.toml
        password = "HelicePower"
        
        # Solicitar a senha de maneira oculta
        input_password = st.text_input("Digite a senha", type="password")

        # Aqui você pode verificar a senha
        if input_password == password:
            st.write("Acesso permitido!")
            with st.form(key="fidelidade", clear_on_submit=True):
                Peso_residuo = 0.0
                Participante = st.text_input("Nome do participante", key="fidelidade")
                Peso_residuo = st.number_input("PESO DO Resíduo Seco (kg)", min_value=0.0, step=0.1, format="%f", value = Peso_residuo)
                
                submited = st.form_submit_button("Salvar")
                if submited:
                    dff = pd.DataFrame()
                    dados = {
                        "Nome": [Participante],
                        "Peso do Resíduo Seco": [Peso_residuo]
                    }
                    dff = pd.DataFrame(dados)
                
                    dff.to_csv("fidelidade.csv", mode="a", header=False,index=False, encoding="utf-8")
                    st.write("Informações salvas!")

            
        else:
            st.write("Senha incorreta!")
        
        
with tab4:
    # Título principal
    st.title("♻️ Dashboard de Triagem de Resíduos Sólidos")
    st.markdown("""
    Bem-vindo ao painel de acompanhamento! Aqui você pode visualizar dados sobre os resíduos triados pelas cooperativas, 
    materiais recebidos da comunidade e rejeitos. Vamos juntos construir um mundo mais sustentável! 🌱
    """)

    # Dados fictícios
    cooperativas = [
        "COOPERTUCA - Cooperativa Campo da Tuca",
        "UTC Lomba do Pinheiro",
        "Centro de Triagem da Vila Pinto"
    ]
    anos = [2022, 2023, 2024]

    # Gerar dados fictícios
    data = {
        "Cooperativa": random.choices(cooperativas, k=100),
        "Ano": random.choices(anos, k=100),
        "Material Recebido (kg)": [random.randint(1000, 8000) for _ in range(100)],
        "Material Triado (kg)": [random.randint(800, 7500) for _ in range(100)],
        "Rejeitos (kg)": [random.randint(100, 1500) for _ in range(100)],
    }

    df = pd.DataFrame(data)

    # Filtros
    st.sidebar.header("Filtros")
    selected_cooperativa = st.sidebar.selectbox("Selecione a Cooperativa", ["Todas"] + cooperativas)
    selected_ano = st.sidebar.selectbox("Selecione o Ano", ["Todos"] + anos)

    # Aplicar filtros
    filtered_df = df.copy()
    if selected_cooperativa != "Todas":
        filtered_df = filtered_df[filtered_df["Cooperativa"] == selected_cooperativa]
    if selected_ano != "Todos":
        filtered_df = filtered_df[filtered_df["Ano"] == selected_ano]

    # KPIs
    st.header("🌟 Indicadores Gerais")
    total_recebido = filtered_df["Material Recebido (kg)"].sum()
    total_triado = filtered_df["Material Triado (kg)"].sum()
    total_rejeitos = filtered_df["Rejeitos (kg)"].sum()
    percentual_triado = (total_triado / total_recebido * 100) if total_recebido > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Material Recebido (kg)", f"{total_recebido:,.0f}")
    col2.metric("Material Triado (kg)", f"{total_triado:,.0f}")
    col3.metric("Rejeitos (kg)", f"{total_rejeitos:,.0f}")
    col4.metric("Percentual Triado (%)", f"{percentual_triado:.2f}%")

    # Tabs
    tab11, tab21, tab31 = st.tabs(["📊 Visualizações", "🌐 Fluxograma", "📋 Dados Detalhados"])

    # Tab 1 - Visualizações
    with tab11:
        # Gráfico de barras
        st.subheader("📊 Material Recebido, Triado e Rejeitos por Cooperativa")
        bar_data = filtered_df.groupby("Cooperativa").sum().reset_index()
        fig_bar = px.bar(
            bar_data,
            x="Cooperativa",
            y=["Material Recebido (kg)", "Material Triado (kg)", "Rejeitos (kg)"],
            barmode="group",
            title="Distribuição de Resíduos por Cooperativa",
            labels={"value": "Quantidade (kg)", "Cooperativa": "Cooperativa"},
            template="plotly_white",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Gráfico de linha
        st.subheader("📈 Evolução Anual da Triagem de Resíduos")
        line_data = filtered_df.groupby("Ano").sum().reset_index()
        fig_line = px.line(
            line_data,
            x="Ano",
            y=["Material Recebido (kg)", "Material Triado (kg)", "Rejeitos (kg)"],
            title="Evolução Anual dos Resíduos",
            labels={"value": "Quantidade (kg)", "Ano": "Ano"},
            markers=True,
            template="plotly_white",
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Gráfico de Meta
        st.subheader("🎯 Meta de Triagem")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=percentual_triado,
            delta={"reference": 80},  # Meta fictícia de 80%
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 50], "color": "red"},
                    {"range": [50, 80], "color": "yellow"},
                ],
            },
            title={"text": "Percentual Triado (%)"},
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Gráfico Sunburst
        st.subheader("🌟 Distribuição de Rejeitos")
        sunburst_data = filtered_df.melt(id_vars=["Cooperativa"], 
                                        value_vars=["Material Recebido (kg)", "Material Triado (kg)", "Rejeitos (kg)"])
        fig_sunburst = px.sunburst(sunburst_data, path=["Cooperativa", "variable"], values="value",
                                title="Distribuição de Resíduos")
        st.plotly_chart(fig_sunburst, use_container_width=True)
        
        # Dados simulados
        data = {
            "Categoria": ["Plástico", "Papel", "Metal", "Vidro", "Orgânico"],
            "Triado (kg)": [1200, 800, 500, 600, 300],
            "Rejeito (kg)": [-200, -150, -80, -100, -50]
        }

        # Criando DataFrame
        df = pd.DataFrame(data)

        # Calculando os valores absolutos e ordenando
        df['Valor Total (absoluto)'] = df['Triado (kg)'] + abs(df['Rejeito (kg)'])
        df = df.sort_values(by='Valor Total (absoluto)', ascending=False)

        # Criando gráfico de funil com particionamento
        figF = go.Figure()

        # Adicionando a parte triada
        figF.add_trace(go.Funnel(
            name="Triado",
            y=df["Categoria"],
            x=df["Triado (kg)"]
        ))

        # Adicionando a parte de rejeitos
        figF.add_trace(go.Funnel(
            name="Rejeito",
            y=df["Categoria"],
            x=abs(df["Rejeito (kg)"])
        ))

        # Configurações do layout
        figF.update_layout(
            title="Funil de Triagem de Resíduos",
            funnelmode="stack",  # Define que as partes serão particionadas
            xaxis_title="Quantidade (kg)",
            yaxis_title="Categorias",
            showlegend=True
        )
        # # Configuração do layout
        # figF.update_layout(
        #     title="Funil de Triagem de Resíduos",
        #     funnelmode="stack",  # Empilhar os valores
        #     legend=dict(title="Categorias")
        # )

        # Mostrar o gráfico
        st.plotly_chart(figF, use_container_width=True)

    # Tab 2 - Fluxograma
    with tab21:
        st.subheader("🌐 Fluxograma de Resíduos")
        st.markdown("O fluxograma será implementado aqui, conectando origens aos destinos.")
        # Adicionar implementação do fluxograma
        # Dados fictícios para o fluxograma
        sources = ["Comunidade", "DMLU", "COOTRAVIPA", "Catadores"]
        destinations = ["COOPERTUCA", "UTC Lomba do Pinheiro", "Centro de Triagem da Vila Pinto"]
        values = [2000, 1500, 1200, 1800, 3000, 2500, 2200, 1700, 2400, 1900, 2000, 1500]

        # Mapear índices de fontes e destinos
        all_nodes = sources + destinations
        node_map = {name: idx for idx, name in enumerate(all_nodes)}

        # Criar fluxos (sources -> destinations)
        sankey_sources = [node_map["Comunidade"], node_map["Comunidade"], node_map["Comunidade"],
                        node_map["DMLU"], node_map["DMLU"], node_map["DMLU"],
                        node_map["COOTRAVIPA"], node_map["COOTRAVIPA"], node_map["COOTRAVIPA"],
                        node_map["Catadores"], node_map["Catadores"], node_map["Catadores"]]
        sankey_targets = [node_map["COOPERTUCA"], node_map["UTC Lomba do Pinheiro"], node_map["Centro de Triagem da Vila Pinto"]] * 4

        # Criar o gráfico de Sankey
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=["#A6CEE3", "#1F78B4", "#B2DF8A", "#33A02C"] + ["#FB9A99", "#E31A1C", "#FDBF6F"],
            ),
            link=dict(
                source=sankey_sources,
                target=sankey_targets,
                value=values,
                color="rgba(31,120,180,0.5)"  # Transparência para os links
            )
        )])

        # Adicionar título e layout
        fig_sankey.update_layout(
            title_text="Fluxograma de Resíduos",
            font_size=10,
            template="plotly_white",
        )

        # Mostrar no Streamlit
        st.subheader("🔄 Fluxograma de Recebimento de Resíduos")
        st.plotly_chart(fig_sankey, use_container_width=True)

    # Tab 3 - Dados Detalhados
    with tab31:
        st.subheader("📋 Dados Detalhados")
        st.dataframe(filtered_df)
with tab5:
    # Função para carregar imagens via URL
    def load_image(url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    # Configuração da página
   # st.set_page_config(page_title="Ranking de Reciclagem", page_icon="♻️", layout="wide")

    # Título e descrição
    st.title("🌟 Ranking de Reciclagem ♻️")
    st.write("Veja as pessoas que mais contribuíram para o nosso projeto de reciclagem sustentável! Obrigado por fazer a diferença pelo meio ambiente. 🌱")

    # Dados fictícios do ranking
    ranking_data = [
        {
            "nome": "Bruna Marquezine",
            "peso": 125.4,
            "residuo": "Plástico",
            "imagem": "https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2025/01/bruna-marquezine-e1736523593544.jpg?w=420&h=240&crop=1&quality=85",
        },
        {
            "nome": "Angelina Jolie",
            "peso": 112.8,
            "residuo": "Papelão",
            "imagem": "https://caras.com.br/media/_versions/2025/01/angelina-jolie_widelg.jpg",
        },
        {
            "nome": "Erick Jacquin",
            "peso": 98.7,
            "residuo": "Vidro",
            "imagem": "https://p2.trrsf.com/image/fget/cf/1200/900/middle/images.terra.com/2024/09/20/948487662-4524440-qual-e-o-doce-favorito-de-erick-jacquin-1400x823-3.jpg",
        },
        {
            "nome": "A Blogueirinha",
            "peso": 84.2,
            "residuo": "Metal",
            "imagem": "https://pbs.twimg.com/media/GOMYD0AXEAEq_m9?format=jpg&name=large",
        },
    ]

    # Exibição do ranking
    st.subheader("🏆 Top Contribuidores")
    cols = st.columns(len(ranking_data))

    for i, pessoa in enumerate(ranking_data):
        with cols[i]:
            # Carregar imagem
            img = load_image(pessoa["imagem"])
            st.image(img, caption=pessoa["nome"])
            # Mostrar informações
            st.markdown(f"**{pessoa['nome']}**")
            st.markdown(f"📦 **Peso doado:** {pessoa['peso']} kg")
            st.markdown(f"🌍 **Resíduo mais doado:** {pessoa['residuo']}")
    
    # Dados fictícios do ranking
    triadores = [
        {"nome": "Maria Silva", "contribuicao": 350, "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkMdWruPwhmCvJIoCqBLc5XBnCrra7es6dnQ&s"},
        {"nome": "Rafaela Pereira", "contribuicao": 300, "foto": "https://newr7-r7-prod.web.arc-cdn.net/resizer/v2/MNSPQTFNABOUZIS77P3R3BKZYU.jpg?auth=d1aff334675165ea6ed39bb652689d98cb89248d1f03400fa1f6716e5d78dfdd&width=460&height=305"},
        {"nome": "Ana Costa", "contribuicao": 280, "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2gyp-hggOmmKOX14WVLvZhul1rKpMBO7Jmw&s"},
        {"nome": "Carlos Souza", "contribuicao": 250, "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEPwfjQ1QXU_aW5_05giaCFm_QhSeG5aQk3g&s"},
    ]

    # Exibir título e descrição
    st.subheader("🏆 Ranking dos Triadores")
    st.write("Confira os triadores que mais contribuíram para a triagem adequada dos resíduos.")

    # Exibir o ranking
    for idx, triador in enumerate(triadores, start=1):
        st.markdown(f"### {idx}º Lugar: {triador['nome']}")
        st.image(triador["foto"], width=150, caption=f"Contribuição: {triador['contribuicao']} kg")
        st.write("---")

    # Elementos de gamificação
    st.markdown("---")
    st.subheader("🎮 Gamificação e Sustentabilidade")
    st.markdown(
        """
        🥇 **Ganhe pontos por cada kg doado!**
        
        🌟 **Troque seus pontos por recompensas ecológicas, como:**
        - Sementes de árvores 🌱
        - Kits de reciclagem doméstica ♻️
        - Descontos em lojas parceiras 💰
        
        🕊️ **Juntos, estamos criando um futuro mais sustentável!**
        """
    )

    # Imagem de sustentabilidade
    sustentabilidade_url = "https://static.todamateria.com.br/upload/su/st/sustentabilidade-og.jpg"
    # sustentabilidade_img = load_image(sustentabilidade_url)
    st.image(sustentabilidade_url,  caption="Faça parte desse movimento!")
with tab6:
    # Título principal
    st.title("♻️ Plataforma de Compra e Venda de Materiais Triados")
    st.markdown("""
    Aqui você pode visualizar os materiais disponíveis para compra ou venda, 
    bem como publicar solicitações de materiais. Juntos podemos fomentar a economia circular! 🌍
    """)

    # Diretório para armazenar as imagens
    image_dir = 'materiais_images/'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Dados fictícios
    cooperativas = [
        "COOPERTUCA - Cooperativa Campo da Tuca",
        "UTC Lomba do Pinheiro",
        "Centro de Triagem da Vila Pinto"
    ]

    materiais = [
        "Plástico PET",
        "Papelão",
        "Vidro",
        "Alumínio",
        "Plástico",
    ]

    # Dados para a publicação de materiais das cooperativas
    cooperativa_data = {
        "Cooperativa": random.choices(cooperativas, k=10),
        "Material": random.choices(materiais, k=10),
        "Preço (R$)": [round(random.uniform(10, 100), 2) for _ in range(10)],
        "Quantidade Disponível (kg)": [random.randint(50, 1000) for _ in range(10)],
        "Foto": [f"{image_dir}material_{i}.jpg" for i in range(10)],
    }

    # Salvar imagens fictícias
    for i in range(10):
        img = Image.new('RGB', (100, 100), color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        img.save(cooperativa_data["Foto"][i])

    df_materiais = pd.DataFrame(cooperativa_data)

    # Seção para publicação de materiais pelas cooperativas
    st.sidebar.header("📢 Publicar Materiais")
    cooperativa_nome = st.sidebar.selectbox("Selecione a Cooperativa", cooperativas)
    material_nome = st.sidebar.selectbox("Selecione o Material", materiais)
    preco = st.sidebar.number_input("Preço (R$)", min_value=0.0, value=10.0, step=0.1)
    quantidade = st.sidebar.number_input("Quantidade Disponível (kg)", min_value=1, value=100, step=1)

    # Carregar imagem do material
    material_img = st.sidebar.file_uploader("Carregar Foto do Material", type=["jpg", "jpeg", "png"])

    if material_img:
        img = Image.open(material_img)
        st.sidebar.image(img, caption="Foto do Material", use_column_width=True)

    # Botão para adicionar o material
    if st.sidebar.button("Publicar Material"):
        new_data = {
            "Cooperativa": cooperativa_nome,
            "Material": material_nome,
            "Preço (R$)": preco,
            "Quantidade Disponível (kg)": quantidade,
            "Foto": f"{image_dir}material_{random.randint(1000, 9999)}.jpg",
        }
        
        df_materiais = df_materiais.append(new_data, ignore_index=True)
        st.sidebar.success("Material publicado com sucesso!")

    # Seção de materiais disponíveis
    st.header("🛒 Materiais Disponíveis para Compra")

    # Filtros de pesquisa
    filtro_material = st.selectbox("Filtrar por Material", ["Todos"] + materiais)
    filtro_cooperativa = st.selectbox("Filtrar por Cooperativa", ["Todas"] + cooperativas)

    # Filtragem dos dados
    df_filtrado = df_materiais.copy()
    if filtro_material != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Material"] == filtro_material]
    if filtro_cooperativa != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Cooperativa"] == filtro_cooperativa]

    # Exibir materiais disponíveis
    for index, row in df_filtrado.iterrows():
        st.subheader(f"📦 {row['Material']} - {row['Cooperativa']}")
        st.image(row["Foto"], width=200)
        st.write(f"**Preço:** R$ {row['Preço (R$)']}")
        st.write(f"**Quantidade Disponível:** {row['Quantidade Disponível (kg)']} kg")
        st.markdown("---")

    # Seção de solicitações de materiais
    st.header("📣 Solicitações de Materiais")

    # Formulário de solicitação
    with st.form(key="solicitacao_form"):
        solicitante_nome = st.text_input("Nome do Solicitante")
        solicitante_material = st.selectbox("Material desejado", materiais)
        solicitante_quantidade = st.number_input("Quantidade desejada (kg)", min_value=1, value=10, step=1)
        submit_button = st.form_submit_button("Publicar Solicitação")

        if submit_button:
            if solicitante_nome:
                st.success(f"Solicitação de {solicitante_quantidade} kg de {solicitante_material} publicada com sucesso!")
            else:
                st.error("Por favor, preencha o nome do solicitante.")

    # Exibir as solicitações de materiais (dados fictícios)
    st.subheader("📝 Solicitações Recentes")

    # Dados de solicitações (fictício)
    solicitacoes = [
        {"Nome": "João Silva", "Material": "Plástico PET", "Quantidade": 200},
        {"Nome": "Maria Oliveira", "Material": "Papelão", "Quantidade": 150},
    ]

    for solicitacao in solicitacoes:
        st.write(f"**{solicitacao['Nome']}** solicita **{solicitacao['Quantidade']} kg** de {solicitacao['Material']}")
        st.markdown("---")

    # Rodapé
    st.markdown("---")
    st.markdown("📢 **Apoie a economia circular e faça a diferença!** 🌍")
with tab7:
    st.title('Dicas Sobre Reciclagem e Sustentabilidade')
    st.video("https://www.youtube.com/watch?v=VmuMSAwXqik")
    st.markdown("### Coleta Seletiva Descomplicada")
    
    st.video("https://www.youtube.com/watch?v=r0uqs18cmtU")
    st.markdown("### Impacto do Lixo Plástico")
    
    st.components.v1.iframe("https://www.jornaldocomercio.com/colunas/pensar-a-cidade/2024/02/1140778-serie-de-reportagens-apresentara-os-caminhos-da-reciclagem-em-porto-alegre.html", width=800, height=1000, scrolling=True)
    st.markdown("### O trabalho das cooperativas de triagem")
