import streamlit as st

import Provas as pv
from pathlib import Path
import base64


def criarLista():


    pv.checaSessoes()

    st.markdown("# :blue[Criação de Lista de Exercícios]")
    "---"
    with st.container(border=True):
        col1, col2 = st.columns([0.5, 1])
        with col1:
            disc = pv.ObterDisciplinas()
            discEscolhida = st.selectbox('Qual a disciplina', disc, key='vdisc')
            topicos = pv.ObterTopicos(discEscolhida)
            topicos = list(topicos[0])

            top = st.multiselect('Seleção de tópico(s)', topicos,default=topicos[0],placeholder='Escolha as opções')
            print(f"TÓPICOS: {top}")
            N=0 # Número de questões por tópico
            Snq = []
            numQ = 0
            i=0
            nTL = []
            for item in top:
                aux = item[0]
                numQ = pv.ObterNumeroQuestoes(discEscolhida, aux)
                Snq.append(numQ)
                N += numQ
                nq1 = st.number_input(f'Número de questões do tópico: {item}',min_value=0, max_value=Snq[i],value=Snq[i],
                            help=f"Nº de questões n={Snq[i]} no banco")
                nTL.append(nq1)
                i += 1
            #st.text(f"Número de questões na Lista:{nTL} ")
            #st.button('Verifica parâmetros', on_click=pv.VerificaParametros, args=(nTL,))

            #if st.session_state.vparm:
            if st.button('Aplicar', on_click=pv.AplicarProva, args=(discEscolhida, nTL,top,'L')):
                st.session_state.chk_status = True
            #st.session_state.bt_status = False
            #else:
            #    ico = ':space_invader:'
            #    st.warning(f'##### Configuração inválida  ou Nº de questões no banco é insuficiente! {ico}')

        with col2:
            check_pdf = st.checkbox('Visualizar PDF', key='chk_status')
            if check_pdf:
                pdf_path = Path('Latex/Cadastro_Questoes/Listas/lista.pdf')
                print(pdf_path)
                base64_pdf = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
                pdf_display = f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1100px" type="application/pdf"></iframe>
                """
                st.markdown(pdf_display, unsafe_allow_html=True)
