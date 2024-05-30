
import streamlit as st


from PIL import Image
import cadastros as cad
import Provas as pv
from pathlib import Path

CAMINHO= Path('Imagens')



def Inicializa():

	logo = Image.open('Imagens/logoDMAT.png')
	st.image(logo, use_column_width=True)
	st.divider()
	st.markdown("# :blue[Cadastro do Sistema]")
	listaOpcoes = ['nenhuma','Incluir / Consultar','Gerar Prova']
	opcao = st.selectbox("Selecione a opção", listaOpcoes)

	if opcao == listaOpcoes[1]:
		pv.checaSessoes()
		cad.cadastros_do_sistema()
	elif opcao == listaOpcoes[3]:
		pv.elaborarProva()
