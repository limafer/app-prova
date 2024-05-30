import streamlit as st
st.set_page_config(page_title='Sistema-Provas', layout='wide', page_icon=':books:')

from streamlit_option_menu import option_menu
import Provas as pv
import cadastros as cad
import Lista as lista

from PIL import Image
# import cadastros as cad
# import Provas as pv
from pathlib import Path

CAMINHO= Path('Imagens')


def Inicializa():

    logo = Image.open('Imagens/logoDMAT.png')
    st.image(logo, use_column_width=True)
    st.divider()
    st.markdown("# :blue[Cadastro do Sistema]")
    listaOpcoes = ['nenhuma','Incluir / Consultar','Alterar / Excluir','Gerar Prova']
    opcao = st.selectbox("Selecione a opção", listaOpcoes)


def main():
    with st.sidebar:
        selected = option_menu("Menu Principal", ["Home", 'Listas','Provas','Exame','Configurações'], icons=['house', 'gear'], menu_icon="cast", default_index=0)
        logo = Image.open('Imagens/logoDMAT.png')
        st.image(logo, use_column_width=True)
        st.divider()
        st.markdown("# :blue[Cadastro do Sistema]")
        listaOpcoes = ['nenhuma','Incluir / Consultar','Alterar / Excluir']
        opcao = st.selectbox("Selecione a opção", listaOpcoes)

    col1,col2 = st.columns([0.1,1])
    with col1:
        imagem = Image.open(CAMINHO / 'imagem2.jpg')
        st.image(imagem)
    with col2:   
        st.markdown('# :blue[Sistema para elaboração de Provas] :books:')
        st.divider()   
		
    if selected == 'Listas':
        lista.criarLista()
    elif selected == 'Provas':
        pv.checaSessoes()
        pv.elaborarProva()
    elif selected == 'Exame':
         pv.elaborarExame()
             
    if opcao == listaOpcoes[1]:
        pv.checaSessoes()
        cad.cadastros_consultas_do_sistema()
    elif opcao == listaOpcoes[2]:
         cad.alteracoes_exclusoes_do_sistema()
          

if __name__ == '__main__':
	main()