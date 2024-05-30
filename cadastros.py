import streamlit as st
import sqlite3
import os, subprocess
import pandas as pd



def geraTexImagem(questao):

        preambulo = r"""
        \documentclass[10pt,a4paper]{article}
        \usepackage[width=16cm]{geometry}
        \usepackage[utf8]{inputenc}
        \usepackage{amsmath}
        \usepackage{amsfonts}
        \usepackage{amssymb}
        \usepackage{graphicx}
        %\usepackage{tikz}
        %\usepackage{tikz-3dplot}
        %\usetikzlibrary{intersections}
        \thispagestyle{empty}
        \usepackage{enumerate}
        \everymath{\displaystyle}
        """

        arqTex = open("Latex/Cadastro_Questoes/img.tex",'w')
        arqTex.write(preambulo)
        arqTex.write('\n\n')
        arqTex.write(r"\begin{document}"+'\n')
        arqTex.write(r'\begin{minipage}[c]{0.5\textwidth}'+'\n')
        arqTex.write(questao+'\n')
        
        arqTex.write(r'\end{minipage}'+'\n\n')
          
        arqTex.write(r'\end{document}')
        arqTex.close()
        gerarImagemPng()




def gerarImagemPng():
        os.chdir("Latex/Cadastro_Questoes/")
        subprocess.run(['pdflatex','img.tex'])

        subprocess.run(['pdfcrop','img.pdf','img.pdf'])
        subprocess.run(['pdftoppm','-png','img.pdf','fig'])

        with st.container(border=True):
            st.image('fig-1.png')
        os.chdir('../../')

        print(os.curdir)
        print(os.path)
    

##################### Funções de Cadastro #############
        

def CadastraAluno(mat,nome,email,disc,curso):
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("INSERT INTO alunos (matricula,nome,email,disciplina,curso) VALUES (?,?,?,?,?)",(mat,nome,email,disc,curso))
    conn.commit()
    conn.close()


def CadastraQuestao(cod, desc):
    desc = desc.lstrip()
    desc = desc.rstrip()
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute(f"SELECT cod_quest FROM questoes WHERE descricao=?",(desc,))
    dado = c.fetchall()
    if dado:
        conn.close()
        st.info('Questão já cadastrada!!')
    else:
        c.execute("INSERT INTO questoes (cod_quest,descricao) VALUES (?,?)",(cod,desc))
        conn.commit()
        conn.close()
        st.info('Questão cadastrada com sucesso!!')

def CadastraDisciplina(_cod, _desc,_cargaH,_hor,_top1='',_top2='',_top3='',_top4='',_top5='',_top6=''):
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("INSERT INTO disciplinas (codigo, descricao,cargaHoraria,horario,topico1,topico2,topico3,topico4,topico5,topico6) \
               VALUES (?,?,?,?,?,?,?,?,?,?)",(_cod,_desc,_cargaH,_hor,_top1,_top2,_top3,_top4,_top5,_top6))
    conn.commit()
    conn.close()

def CadastraUsuario(nome, senha, email):
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",(nome,senha,email))
    conn.commit()
    conn.close()



######################## Consultas #############################
        
def ConsultaUsuarios():
    diretorio = os.getcwd()
    print(diretorio)
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def ConsultaAlunos():
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM alunos")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def ConsultaDisciplinas():
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM disciplinas")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def ConsultaQuestoes():
    conn = sqlite3.connect('databaseProvas.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questoes")
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

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




def alteracoes_exclusoes_do_sistema():
     # st.markdown('# :blue[Cadastros e Consultas do Sistema]')
    # st.divider()

    container = st.container()

    with container:
        col1,col2 = st.columns([0.7,1])
        with col1:

            st.header('Selecione a Alteração')
            cad = st.selectbox("",['Nenhuma opção','Alterar Usuários','Alterar Questões','Alterar Alunos','Alterar Disciplina'])

            if cad == 'Alterar Alunos':
                with st.form('Alteração de Alunos',clear_on_submit=True):
                    matricula = st.text_input('Matricula')
                    nome = st.text_input('Nome')
                    email = st.text_input('E-mail')
                    disciplina = st.text_input('Disciplina')
                    curso = st.text_input('Curso')
                        #senha = st.text_input('Senha')
                        #confirmacao = st.text_input('Confirmar Senha')
                    if st.form_submit_button('Alterar'):
                        if nome == '' or matricula == '' or email == '' or disciplina == '' or curso == '':
                            st.error('Preencha todos os campos')
                        else:
                            CadastraAluno(matricula,nome,email,disciplina,curso)
                            st.success('Cadastro realizado com sucesso')

            if cad == 'Incluir Questões':
                lista_disciplinas = ConsultaDisciplinas()
                lista_res = []
                for ind in lista_disciplinas:
                    lista_res.append(ind[1]+'-'+ind[2])
                disciplina = str(st.selectbox('Entre com o código da disciplina',lista_res))
                topicos = ObterTopicos(disciplina)
                topicos = topicos[0]
                topico = st.selectbox('Tópico',topicos)
                questao = st.text_area('Entre com o texto da questão em $\LaTeX$',placeholder='$\displaystyle\int f(x)dx$',key='res',value=st.session_state.texto_area)
                codquest = disciplina.split('-')[0]  + str(topico[0])

                on = st.toggle('Compila questão', value=st.session_state.status_tog)

                if on:
                    if questao:
                        geraTexImagem(questao)
                        st.session_state.texto_area = questao
                        st.write('Questão visualizada!')
                        check = st.checkbox('Cadastra a questão?',value=st.session_state.status_chk)
                        if check:
                            CadastraQuestao(codquest,questao)
                            # st.session_state.texto_area = ""
                            # st.session_state.status_tog = False
                            # st.session_state.status_chk = False

                        else:
                            st.session_state.texto_area = ""
                            st.write('Entre com a questão!')
                    else:
                        st.warning("Entre com o texto da questão primeiro!!")
                else:
                    st.warning("Habilite o botão de compilação!!")



            elif cad == 'Incluir Usuários':
                with st.form(':blue[Cadastro de Usuários]',clear_on_submit=True):
                    nome = st.text_input('Nome')
                    email = st.text_input('E-mail')
                    senha = st.text_input('Senha',type='password')
                    confirmacao = st.text_input('Confirmar Senha',type='password')
                    if st.form_submit_button('Cadastrar'):
                        if nome == '' or email == '' or senha == '' or confirmacao == '':
                            st.error('Preencha todos os campos')
                        elif senha != confirmacao:
                            st.error('As senhas não conferem')
                        else:
                            CadastraUsuario(nome,senha,email)
                            st.success('Cadastro realizado com sucesso')

            elif cad == 'Incluir Disciplina':
                with st.form('Cadastro de Disciplina'):
                    codigo = st.text_input('Código').upper()
                    print(codigo)
                    descricao = st.text_input('Descrição')
                    cargaHoraria = st.text_input('Carga Horária')
                    horario = st.selectbox('Horário',['24T12','24T34','24M12','24M34','35T12','35T34','35M12','35M34','24N12','24N34','35N12','35N34'])
                    with st.expander('Tópicos'):
                        top1 = st.text_input('Tópico 1')
                        top2 = st.text_input('Tópico 2')
                        top3 = st.text_input('Tópico 3')
                        top4 = st.text_input('Tópico 4')
                        top5 = st.text_input('Tópico 5')
                        top6 = st.text_input('Tópico 6')
                    if st.form_submit_button('Cadastrar'):
                        if codigo == '' or descricao == '' or cargaHoraria=='':
                            st.error('Preencha todos os campos')
                        else:
                            CadastraDisciplina(codigo,descricao,cargaHoraria,horario,top1,top2,top3,top4,top5,top6)
                            st.success('Cadastro realizado com sucesso')
        with col2:
            st.header('Selecione a consulta')
            select = st.selectbox('',['Nenhuma seleção','Usuários','Alunos','Questões','Disciplinas'])
            if select == 'Usuários':
                usuarios = ConsultaUsuarios()
                st.dataframe(usuarios,hide_index=True,width=900)
            if select == 'Alunos':
                alunos = ConsultaAlunos()
                df_alunos = pd.DataFrame(alunos,columns=('Id','Matrícula','Nome','e-mail','Disciplina','Curso'))
                st.dataframe(df_alunos,width=900)
            elif select == 'Questões':
                questoes = ConsultaQuestoes()
                df = pd.DataFrame(questoes, columns=('Id', 'Código', 'Descrição'))
                st.dataframe(df,hide_index=True,width=700)
            elif select == 'Disciplinas':
                disciplinas = ConsultaDisciplinas()
                df = pd.DataFrame(disciplinas, columns=('Id', 'Código', 'Descrição','Carga Horária','Horário','Tópico 1','Tópico 2','Tópico 3','Tópico 4','Tópico 5','Tópico 6'))
                st.dataframe(df,hide_index=True)




def cadastros_consultas_do_sistema():
    # st.markdown('# :blue[Cadastros e Consultas do Sistema]')
    # st.divider()

    container = st.container()

    with container:
        col1,col2 = st.columns([0.5,1])
        with col1:

            st.header('Selecione a Inclusão')
            cad = st.selectbox("",['Nenhuma opção','Incluir Usuários','Incluir Questões','Incluir Alunos','Incluir Disciplina'])

            if cad == 'Incluir Alunos':
                with st.form('Inclusão de Alunos',clear_on_submit=True):
                    matricula = st.text_input('Matricula')
                    nome = st.text_input('Nome')
                    email = st.text_input('E-mail')
                    disciplina = st.text_input('Disciplina')
                    curso = st.text_input('Curso')
                        #senha = st.text_input('Senha')
                        #confirmacao = st.text_input('Confirmar Senha')
                    if st.form_submit_button('Cadastrar'):
                        if nome == '' or matricula == '' or email == '' or disciplina == '' or curso == '':
                            st.error('Preencha todos os campos')
                        else:
                            CadastraAluno(matricula,nome,email,disciplina,curso)
                            st.success('Cadastro realizado com sucesso')

            if cad == 'Incluir Questões':
                lista_disciplinas = ConsultaDisciplinas()
                lista_res = []
                for ind in lista_disciplinas:
                    lista_res.append(ind[1]+'-'+ind[2])
                disciplina = str(st.selectbox('Entre com o código da disciplina',lista_res))
                topicos = ObterTopicos(disciplina)
                topicos = topicos[0]
                topico = st.selectbox('Tópico',topicos)
                questao = st.text_area('Entre com o texto da questão em $\LaTeX$',placeholder='$\displaystyle\int f(x)dx$',key='res',value=st.session_state.texto_area)
                codquest = disciplina.split('-')[0]  + str(topico[0])

                on = st.toggle('Compila questão', value=st.session_state.status_tog)

                if on:
                    if questao:
                        geraTexImagem(questao)
                        st.session_state.texto_area = questao
                        st.write('Questão visualizada!')
                        check = st.checkbox('Cadastra a questão?',value=st.session_state.status_chk)
                        if check:
                            CadastraQuestao(codquest,questao)
                            # st.session_state.texto_area = ""
                            # st.session_state.status_tog = False
                            # st.session_state.status_chk = False

                        else:
                            st.session_state.texto_area = ""
                            st.write('Entre com a questão!')
                    else:
                        st.warning("Entre com o texto da questão primeiro!!")
                else:
                    st.warning("Habilite o botão de compilação!!")



            elif cad == 'Incluir Usuários':
                with st.form(':blue[Cadastro de Usuários]',clear_on_submit=True):
                    nome = st.text_input('Nome')
                    email = st.text_input('E-mail')
                    senha = st.text_input('Senha',type='password')
                    confirmacao = st.text_input('Confirmar Senha',type='password')
                    if st.form_submit_button('Cadastrar'):
                        if nome == '' or email == '' or senha == '' or confirmacao == '':
                            st.error('Preencha todos os campos')
                        elif senha != confirmacao:
                            st.error('As senhas não conferem')
                        else:
                            CadastraUsuario(nome,senha,email)
                            st.success('Cadastro realizado com sucesso')

            elif cad == 'Incluir Disciplina':
                with st.form('Cadastro de Disciplina'):
                    codigo = st.text_input('Código').upper()
                    print(codigo)
                    descricao = st.text_input('Descrição')
                    cargaHoraria = st.text_input('Carga Horária')
                    horario = st.selectbox('Horário',['24T12','24T34','24M12','24M34','35T12','35T34','35M12','35M34','24N12','24N34','35N12','35N34'])
                    with st.expander('Tópicos'):
                        top1 = st.text_input('Tópico 1')
                        top2 = st.text_input('Tópico 2')
                        top3 = st.text_input('Tópico 3')
                        top4 = st.text_input('Tópico 4')
                        top5 = st.text_input('Tópico 5')
                        top6 = st.text_input('Tópico 6')
                    if st.form_submit_button('Cadastrar'):
                        if codigo == '' or descricao == '' or cargaHoraria=='':
                            st.error('Preencha todos os campos')
                        else:
                            CadastraDisciplina(codigo,descricao,cargaHoraria,horario,top1,top2,top3,top4,top5,top6)
                            st.success('Cadastro realizado com sucesso')
        with col2:
            st.header('Selecione a consulta')
            select = st.selectbox('',['Nenhuma seleção','Usuários','Alunos','Questões','Disciplinas'])
            if select == 'Usuários':
                usuarios = ConsultaUsuarios()
                st.dataframe(usuarios,hide_index=True,width=900)
            if select == 'Alunos':
                alunos = ConsultaAlunos()
                df = pd.DataFrame(alunos,columns=('Id','Matrícula','Nome','e-mail','Disciplina','Curso'))
                st.dataframe(df,hide_index=True,width=900)
            elif select == 'Questões':
                questoes = ConsultaQuestoes()
                df = pd.DataFrame(questoes, columns=('Id', 'Código', 'Descrição'))
                st.dataframe(df,hide_index=True,width=900)
            elif select == 'Disciplinas':
                disciplinas = ConsultaDisciplinas()
                df = pd.DataFrame(disciplinas, columns=('Id', 'Código', 'Descrição','Carga Horária','Horário','Tópico 1','Tópico 2','Tópico 3','Tópico 4','Tópico 5','Tópico 6'))
                st.dataframe(df,hide_index=True)

