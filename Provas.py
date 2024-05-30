import pandas as pd
import streamlit as st

import sqlite3
import random
import os, subprocess
from streamlit_modal import Modal
import base64
#from streamlit_pdf_viewer import pdf_viewer
from pathlib import Path

dir_atual = os.getcwd()

listaQuestoes = []
listaQuestoesProva=[]
# st.markdown('# :blue[Elaboração automática de provas ]  :book:')
# "---"

def checaSessoes():

    if 'chk_disable' not in st.session_state:
        st.session_state.chk_disable = True 

    if 'status_chk' not in st.session_state:
        st.session_state.status_chk = False

    if 'status_tog' not in st.session_state:
        st.session_state.status_tog = False

    if 'selecao_mista' not in st.session_state:
        st.session_state.selecao_mista = False
        st.session_state.prova = []

    if 'texto_area' not in st.session_state:
        st.session_state.texto_area = ""

    if not 'nqt' in st.session_state:
        st.session_state.nqt=0

    if not 'vparm' in st.session_state:
        st.session_state.vparm=False

    if not 'chk_status' in st.session_state:
        st.session_state.chk_status = False

    if not 'top_c' in st.session_state:
        st.session_state.top_c=''

    if not 'listaQ' in st.session_state:
        st.session_state.listaQ=[]



def VerificaParametros(nq):
    if nq:
        st.session_state.vparm = True
    else:
        st.session_state.vparm = False

def ObterQuestoes(sql):
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute(sql[0],sql[1])
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def ObterQuestoes_Selecionadas(sql):
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute(sql)
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data


@st.experimental_dialog("Selecione as questões",width='large')
def selecionaQuestoesEspecificas(discEscolhida,nq,top):
            
                    
    std = discEscolhida.split('-')[0].rstrip()

    if nq > 0:
        cod = None
        cod = std  + top[0]
        sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
        dados = ObterQuestoes(sql)
        n = len(dados)
        col1,col2 = st.columns([0.15,1])
        count  = 0
        nq_ale = 0
        st.session_state.prova.clear()
        with st.container():
            for i in range(n):
                
                with col1:
                    if st.checkbox(str(i+1)):
                        count += 1
                        st.session_state.prova.append(dados[i][0])
                with col2:
                        st.write(dados[i][0])

            if count < nq:
                nq_ale = nq - count

        st.session_state.chk_disable = False
        if st.button("Aplica Prova"):
            AplicarProva(discEscolhida,nq_ale,top,'M')
        


#questoes = ObterQuestoes("SELECT descricao FROM questoes")


def ObterDisciplinas():
    lista = []
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT codigo,descricao FROM disciplinas")
    data = c.fetchall()
    conn.commit()
    conn.close()
    for dados in data:
        lista.append(dados[0] + '-' + dados[1])
    return lista

def ObterTopicos(disc):
    cod = disc.split('-')[0]
    lista = []
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT topico1,topico2,topico3 FROM disciplinas WHERE codigo =?",(cod,))
    data = c.fetchall()
    conn.commit()
    conn.close()
    for dados in data:
        lista.append(dados)
    return lista

def ObterNumeroQuestoes(disc,fid):
    cod = disc.split('-')[0]
    cod += fid
    lista = []
    numF,numI,numD, numR = 0,0,0,0
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT cod_quest FROM questoes WHERE cod_quest=?",(cod,))
    data = c.fetchall()
    conn.commit()
    conn.close()
    for dados in data:
        lista.append(dados[0])
    for qt in lista:
        if qt[-2] == 'F':
            numR +=1
        elif qt[-2] == 'I':
            numR += 1
        else:
            numR += 1
    return numR


def AplicarProva(discEsc,nq,top,tipo):
    if tipo == 'M':
        std = discEsc.split('-')[0].rstrip()

        if nq > 0:

            cod = None
            cod = std  + top[0]
            sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
            dados = ObterQuestoes(sql)
            
            for i in range(nq):
                qt = random.choices(dados)
                if qt[0][0] not in st.session_state.prova:
                    st.session_state.prova.append(qt[0][0])
                else:
                    while qt[0][0] in st.session_state.prova:
                        qt = random.choices(dados)
                    st.session_state.prova.append(qt[0][0])
            print(st.session_state.prova)

        for i in range(len(st.session_state.prova)):
            listaQuestoesProva.append(st.session_state.prova[i])

        print(listaQuestoesProva)

        st.session_state.chk_disable = False

        gerarCodigoLatex('M')
        gerarArquivoPDF('M')

    if tipo == 'P':
        std = discEsc.split('-')[0].rstrip()
        prova = []

        if nq > 0:

            cod = None
            cod = std  + top[0]
            sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
            dados = ObterQuestoes(sql)
            n = len(dados)
            for i in range(nq):
                qt = random.choices(dados)
                if qt not in prova:
                    prova.append(qt)
                else:
                    while qt in prova:
                        qt = random.choices(dados)
                    prova.append(qt)

            print(prova)
        for i in range(len(prova)):
            for j in range(len(prova[i])):
                listaQuestoesProva.append(prova[i][j][0])

        st.session_state.chk_disable = False

        print(listaQuestoesProva)
        gerarCodigoLatex('P')
        gerarArquivoPDF('P')
    elif tipo == 'L':
        print(f"Número de questões da Lista:{nq}")
        std = discEsc.split('-')[0].rstrip()
        lista = []

        if nq:
            j=0
            for item in top:
                cod = None
                cod = std  + item[0][0]
                sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
                dados = ObterQuestoes(sql)
                n = len(dados)
                for i in range(nq[j]):
                    qt = random.choices(dados)  # , weights = [1]*n)# k = nFacil)
                    if qt not in lista:
                        lista.append(qt)
                    else:
                        while qt in lista:
                            qt = random.choices(dados)
                        lista.append(qt)
                j += 1
        for i in range(len(lista)):
            for j in range(len(lista[i])):
                listaQuestoes.append(lista[i][j][0])

        gerarCodigoLatex('L')
        gerarArquivoPDF('L')
    elif tipo == 'E':
        print(f"Número de questões da Lista:{nq}")
        std = discEsc.split('-')[0].rstrip()
        lista = []

        if nq:
            j=0
            for item in top:
                cod = None
                cod = std  + item[0][0]
                print(cod)
                sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
                dados = ObterQuestoes(sql)
                n = len(dados)
                for i in range(nq[j]):
                    qt = random.choices(dados)  # , weights = [1]*n)# k = nFacil)
                    if qt not in lista:
                        lista.append(qt)
                    else:
                        while qt in lista:
                            qt = random.choices(dados)
                        lista.append(qt)
                j += 1
                print("Listando as questões")
                print(lista)
        for i in range(len(lista)):
            for j in range(len(lista[i])):
                listaQuestoes.append(lista[i][j][0])

        print(listaQuestoes)
        gerarCodigoLatex('L')
        gerarArquivoPDF('L')



def gerarCodigoLatex(tipo):
    nomeAtividade = ''
    if tipo == 'P' or tipo == 'M':
        nomeAtividade = 'prova.tex'
    elif tipo == 'L':
        nomeAtividade = 'lista.tex'

    preambulo = r"""
    \documentclass[12pt,a4paper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath}
    \usepackage{amsfonts}
    \usepackage{amssymb}
    \usepackage{graphicx}
    %\usepackage{tikz}
    %\usepackage{tikz-3dplot}
    \usepackage{enumerate}
    %\usetikzlibrary{intersections}
    \usepackage[left=2.0cm,top=1.5cm,right=2.0cm]{geometry}
    \newcommand{\edo}[3]{$#1\,{\rm{d}}x#2\,{\rm{d}}y=#3$}
    \thispagestyle{empty}
    
    \everymath{\displaystyle}
    """

    if tipo == 'P' or tipo == 'M':
        diret = 'Latex/Cadastro_Questoes/Provas/'
    else:
        diret = 'Latex/Cadastro_Questoes/Listas/'

    arqTex = open(diret + nomeAtividade, 'w')
    arqTex.write(preambulo)
    arqTex.write('\n\n')
    arqTex.write(r"\begin{document}" + '\n')
    arqTex.write(r"\begin{center}" + '\n')
    disciplina = str(st.session_state.vdisc).split('-')[1]
    if tipo == 'P' or tipo == 'M':
        arqTex.write(r"\large AVALIAÇÃO DE {0}\\".format(disciplina) + '\n')
        arqTex.write(r"{\large\bf Departamento de Matemática}\\[1mm] \textit{Prof. Lindeval: lindeval.ufrr@gmail.com}\\" + r"\end{center}" + '\n\n')
        arqTex.write(r"\noindent Nome: \rule{9cm}{0.3mm}\ \ Matrícula: \rule{3.5cm}{0.3mm}\\[1cm]" + '\n')
    elif tipo == 'L':
        arqTex.write(r"\large LISTA DE EXERCÍCIOS DE {0}\\[1mm]".format(disciplina) + '\n')
        arqTex.write(r"{\large\bf Departamento de Matemática}\\[1mm] \textit{Prof. Lindeval: lindeval.ufrr@gmail.com}\\" + r"\end{center}" + '\n\n')
        arqTex.write(r"\noindent\rule{17.0cm}{0.7mm}\\[0.5cm]" + '\n')

    if tipo == 'P':
        for i in range(len(listaQuestoesProva)):
            arqTex.write(r"\noindent" + '\n')
            arqTex.write("{0}) ".format(i + 1))
            arqTex.write(listaQuestoesProva[i])
            if "begin" in listaQuestoesProva[i]:
                arqTex.write('\n')
            else:
                arqTex.write(r"\\" + '\n')

        arqTex.write(r"\vfill\hfill\bf{\textit{Boa Sorte!}}" + '\n')
        arqTex.write(r"\end{document}")

        listaQuestoesProva.clear()
        arqTex.close()
    elif tipo == 'L':
        for i in range(len(listaQuestoes)):
            arqTex.write(r"\noindent" + '\n')
            arqTex.write("{0}) ".format(i + 1))
            arqTex.write(listaQuestoes[i])
            if "begin" in listaQuestoes[i]:
                arqTex.write('\n')
            else:
                arqTex.write(r"\\[2mm]" + '\n')

        arqTex.write(r"\vfill\hfill\bf{\textit{Boas Atividades!}}" + '\n')
        arqTex.write(r"\end{document}")

        listaQuestoes.clear()
        arqTex.close()
    elif tipo == 'M':
        for i in range(len(listaQuestoesProva)):
            arqTex.write(r"\noindent" + '\n')
            arqTex.write("{0}) ".format(i + 1))
            arqTex.write(listaQuestoesProva[i])
            print(type(listaQuestoesProva[i]))
            if "begin" in listaQuestoesProva:
                arqTex.write('\n')
            else:
                arqTex.write(r"\\" + '\n')

        arqTex.write(r"\vfill\hfill\bf{\textit{Boa Sorte!}}" + '\n')
        arqTex.write(r"\end{document}")

        listaQuestoesProva.clear()
        arqTex.close()


def gerarArquivoPDF(tipo):

    if tipo == 'P' or tipo == 'M':
        os.chdir('Latex/Cadastro_Questoes/Provas/')
        subprocess.run(['pdflatex', 'prova.tex'])
    else:
        os.chdir('Latex/Cadastro_Questoes/Listas/')
        subprocess.run(['pdflatex', 'lista.tex'])
    os.chdir('../../../')


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 100%; height: 200%;">"""

    # Displaying File
    return pdf_display

@st.experimental_dialog("Selecione as questões",width='large')
def selecionaQuestoes(discEscolhida,nq,top):
    st.session_state.chk_disable = True
            
                    
    std = discEscolhida.split('-')[0].rstrip()
    prova = []

    if nq > 0:
        cod = None
        cod = std  + top[0]
        sql = 'SELECT descricao FROM questoes WHERE cod_quest=?', (cod,)
        dados = ObterQuestoes(sql)
        n = len(dados)
        col1,col2 = st.columns([0.15,1])
        count =0
        with st.container():
            for i in range(n):
                
                with col1:
                    if st.checkbox(str(i+1)):
                        count += 1
                        prova.append(dados[i][0])
                with col2:
                        st.write(dados[i][0])


        for i in range(count):
            listaQuestoesProva.append(prova[i])

        gerarCodigoLatex('P')
        gerarArquivoPDF('P')
        st.session_state.chk_disable = False
        if st.button("ok"):
                     st.rerun()
        

def elaborarProva():

    checaSessoes()

    with st.container(border=True):
        col1,col2 = st.columns([0.4,1])
        with col1:
            disc = ObterDisciplinas()
            discEscolhida = st.selectbox('Qual a disciplina',disc, key='vdisc',)
            topicos = ObterTopicos(discEscolhida)
            topicos = list(topicos[0])

            top = st.selectbox('Seleção de tópico(s)', topicos, placeholder='Escolha as opções')
            aux = top[0]

            tipo = 'P'
            numQ = ObterNumeroQuestoes(discEscolhida, aux) # obtém número de questões no banco

            nq = st.number_input('Número de questões', min_value=1, max_value=numQ, value=1,help=f"Nº de questões no banco: ({numQ})")

            modal = Modal(key="key_sel",title="Seleção de questões para a prova",max_width=700)
            st.write("Selecione o modo de escolha das questões")
            #open_modal = st.button("Seleção manual")
            if st.button("Seleção aleatória",help='Seleciona de forma aleatória as questões no banco no tópico escolhido!'):
                st.write('As questões foram selecionadas aleatoriamente!')
                if st.button('Aplicar',on_click=AplicarProva, args=(discEscolhida,nq,top,tipo)):
                    st.session_state.chk_status = True
                    st.session_state.chk_disable = False

            if st.button('Seleção Mista',help='Seleciona questões obrigatórias na prova e sorteia as outras aleatoriamente!'):
                st.session_state.chk_disable = False
                selecionaQuestoesEspecificas(discEscolhida,nq,top)

            #if open_modal:
            #    st.session_state.chk_disable = False
            #    selecionaQuestoes(discEscolhida,nq,top)

        with col2:    
                    
            check_pdf = st.checkbox('Visualizar PDF',key='chk_status',disabled=st.session_state.chk_disable)
            if check_pdf:
                pdf_path = Path('Latex/Cadastro_Questoes/Provas/prova.pdf')
                base64_pdf = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
                pdf_display=f"""
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="1100px" type="application/pdf"></iframe>
                """
                st.markdown(pdf_display, unsafe_allow_html=True)
                st.session_state.chk_disable = True

                         
def elaborarExame():
    
    checaSessoes()

    st.markdown("# :blue[Elaborar exame final]")
    "---"
    with st.container(border=True):
        col1, col2 = st.columns([0.5, 1])
        with col1:
            disc = ObterDisciplinas()
            discEscolhida = st.selectbox('Qual a disciplina', disc, key='vdisc')
            topicos = ObterTopicos(discEscolhida)
            topicos = list(topicos[0])

            top = st.multiselect('Seleção de tópico(s)', topicos,default=topicos[0],placeholder='Escolha as opções')
            N=0 # Número de questões por tópico
            Snq = []
            numQ = 0
            i=0
            nTL = []
            for item in top:
                aux = item[0]
                numQ = ObterNumeroQuestoes(discEscolhida, aux)
                Snq.append(numQ)
                N += numQ
                nq1 = st.number_input(f'Número de questões do tópico: {item}',min_value=0, max_value=Snq[i],value=Snq[i],
                            help=f"Nº de questões n={Snq[i]} no banco")
                nTL.append(nq1)
                i += 1
           
            # if st.checkbox('Selecionar questões específicas?'):
            #     selecionaQuestoesEspecíficas(discEscolhida,)

            if st.button('Aplicar', on_click=AplicarProva, args=(discEscolhida, nTL,top,'E')):
                st.session_state.chk_status = True
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
