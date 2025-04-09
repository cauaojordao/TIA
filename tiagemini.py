from xhtml2pdf import pisa
import os
import re
import markdown2
from PyPDF2 import PdfReader
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = "gemini-1.5-flash"

def configurar_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(MODEL_NAME)

def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor = PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text()
        return texto

def gerar_resumo_gemini(model, texto):
    prompt = f"""
    Crie um resumo acadêmico detalhado do seguinte texto, 
    organizando as informações em tópicos lógicos e destacando:
    - Conceitos fundamentais
    - Definições importantes
    - Relações entre ideias
    - Exemplos relevantes
    
    O resumo deve ser completo o suficiente para servir como material de estudo autônomo.

    Texto:
    {texto[:30000]}
    """
    response = model.generate_content(prompt)
    return response.text

def gerar_questoes_gemini(model, texto_resumido):
    prompt = f"""
    Com base no seguinte resumo, crie EXATAMENTE 10 questões de múltipla escolha seguindo ESTE FORMATO:

    --- INÍCIO DO FORMATO ---
    1. [Enunciado claro da questão]
    a) [Alternativa A] (correta)
    b) [Alternativa B]
    c) [Alternativa C]
    d) [Alternativa D]
    --- FIM DO FORMATO ---

    REGRAS:
    1. Cada questão deve ter 4 alternativas
    2. Apenas UMA alternativa correta por questão, marcada com "(correta)"
    
    IMPORTANTE: Mantenha exatamente o formato descrito. A palavra (correta) deve aparecer SEMPRE ao lado da alternativa correta, exatamente assim: "a) conteúdo da alternativa (correta)"
    
    3. Alternativas erradas devem ser plausíveis
    4. Variar o posicionamento da alternativa correta
    5. Focar nos conceitos mais importantes do resumo
    6. Não usar "Todas as anteriores" ou "Nenhuma das anteriores"

    Resumo:
    {texto_resumido[:20000]}
    """
    response = model.generate_content(prompt)
    return response.text

def processar_gabarito(questoes):
    gabarito = []
    numero_questao = None

    linhas = questoes.split('\n')
    for linha in linhas:
        linha = linha.strip()
        match_q = re.match(r'^(\d+)\.\s', linha)
        if match_q:
            numero_questao = match_q.group(1)
        match_alt = re.match(r'^([a-dA-D])\)\s.*\(?correta\)?', linha, re.IGNORECASE)
        if match_alt and numero_questao:
            letra = match_alt.group(1).upper()
            gabarito.append(f"{numero_questao}. {letra}")
    return gabarito

def gerar_html(resumo_md, questoes_md, gabarito, titulo="Material de Estudo"):
    # Processa tabelas no resumo antes de converter para HTML
    resumo_com_tabelas = processar_tabelas_markdown(resumo_md)
    resumo_html = markdown2.markdown(resumo_com_tabelas)
    
    # Resto da função permanece igual
    gabarito_html = "<br>".join(gabarito)

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            /* Configurações gerais do documento */
            body {{
                font-family: 'Helvetica Neue', Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                margin: 1.5cm;
                color: #333;
            }}
            
            /* Títulos */
            h1 {{
                font-size: 14pt;
                font-weight: 600;
                text-align: center;
                margin: 20px 0;
                padding-bottom: 8px;
                border-bottom: 1px solid #e1e1e1;
                color: #2c3e50;
            }}
            
            h2 {{
                font-size: 12pt;
                font-weight: 600;
                margin: 18px 0 12px 0;
                color: #2c3e50;
                border-bottom: 1px solid #f0f0f0;
                padding-bottom: 4px;
            }}
            
            /* Texto e parágrafos */
            p {{
                margin: 0 0 8px 0;
                text-align: left;
            }}
            
            /* Listas */
            ol, ul {{
                margin: 8px 0 12px 20px;
                padding: 0;
                list-style-type: lower-alpha;
            }}
            
            li {{
                margin-bottom: 6px;
            }}
            
            /* Questões e alternativas */
            .question {{
                margin-bottom: 16px;
            }}
            
            .question-text {{
                font-weight: 500;
                margin-bottom: 8px;
            }}
            
            
            /* Gabarito */
            .answer-key {{
                margin-top: 24px;
                padding: 12px;
                background-color: #f8f8f8;
                border: 1px solid #e0e0e0;
                font-size: 10pt;
            }}
            
            .answer-key h2 {{
                margin-top: 0;
            }}
            
            /* Blocos de código (se necessário) */
            .code {{
                font-family: 'Courier New', monospace;
                font-size: 10pt;
                background-color: #f9f9f9;
                padding: 8px;
                margin: 8px 0;
                border: 1px solid #ddd;
                border-radius: 3px;
                overflow-x: auto;
            }}
            
             /* Estilos específicos para tabelas */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 12px 0;
                font-size: 10pt;
                page-break-inside: avoid;  /* Evita quebras de página dentro da tabela */
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 6px 8px;
                text-align: left;
                vertical-align: top;
            }}
            
            th {{
                background-color: #f2f2f2;
                font-weight: 600;
            }}
            
            /* Forçar quebra de palavras longas */
            td {{
                word-wrap: break-word;
                overflow-wrap: break-word;
            }}
            
            /* Melhorar espaçamento em células */
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            /* Espaçamento entre seções */
            .section {{
                margin-bottom: 24px;
            }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        
        <div class="section">
            <h2>Resumo</h2>
            {resumo_html}
        </div>
        
        <div class="section">
            <h2>Questões</h2>
            {questoes_md}
        </div>
        
        <div class="answer-key">
            <h2>Gabarito</h2>
            {gabarito_html}
        </div>
    </body>
    </html>
    """
    return html

def processar_tabelas_markdown(texto_md):
    # Expressão regular para encontrar tabelas no Markdown
    padrao_tabela = re.compile(
        r'(\n\n|^)([^\n]*\|[^\n]*\n)([^\n]*\|[^\n]*\n)(([^\n]*\|[^\n]*\n)*)',
        re.MULTILINE
    )
    
    def substituir_tabela(match):
        linhas = match.group(0).strip().split('\n')
        
        # Remove linhas vazias e espaços extras
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        
        # Processa cabeçalho e separador
        cabecalho = linhas[0].split('|')
        separador = linhas[1].split('|')
        
        # Verifica alinhamento
        alinhamentos = []
        for col in separador:
            col = col.strip()
            if col.startswith(':') and col.endswith(':'):
                alinhamentos.append('center')
            elif col.startswith(':'):
                alinhamentos.append('left')
            elif col.endswith(':'):
                alinhamentos.append('right')
            else:
                alinhamentos.append('left')
        
        # Processa linhas de dados
        linhas_dados = linhas[2:]
        
        # Gera HTML da tabela
        html = ['<table>']
        
        # Cabeçalho
        html.append('<thead><tr>')
        for i, col in enumerate(cabecalho):
            col = col.strip()
            if col:  # Ignora colunas vazias no início/fim
                html.append(f'<th style="text-align:{alinhamentos[i]}">{col}</th>')
        html.append('</tr></thead>')
        
        # Corpo
        html.append('<tbody>')
        for linha in linhas_dados:
            html.append('<tr>')
            colunas = linha.split('|')
            for i, col in enumerate(colunas):
                col = col.strip()
                if col:  # Ignora colunas vazias no início/fim
                    html.append(f'<td style="text-align:{alinhamentos[i]}">{col}</td>')
            html.append('</tr>')
        html.append('</tbody>')
        
        html.append('</table>')
        return ''.join(html)
    
    # Substitui todas as tabelas no texto
    return padrao_tabela.sub(substituir_tabela, texto_md)


def formatar_questoes_para_html(questoes_raw):
    linhas = questoes_raw.strip().split("\n")
    questoes_html = ""
    numero = 0

    for linha in linhas:
        linha = linha.strip()
        if re.match(r'^\d+\.\s', linha):
            if numero > 0:
                questoes_html += "</ul></li>\n"  # fecha questão anterior
            numero += 1
            enunciado = re.sub(r'^\d+\.\s*', '', linha)
            questoes_html += f"<li><p><strong>{numero}. {enunciado}</strong></p>\n<ul>\n"
        elif re.match(r'^[a-dA-D]\)', linha):
            alternativa = re.sub(r'^[a-dA-D]\)\s*', '', linha)
            questoes_html += f"<li>{alternativa}</li>\n"
        else:
            questoes_html += f"<p>{linha}</p>"

    if numero > 0:
        questoes_html += "</ul></li>\n"  # fecha última questão

    return f"<ol>\n{questoes_html}</ol>"


def salvar_pdf_html(html, caminho_saida):
    from xhtml2pdf import pisa
    from io import StringIO, BytesIO

    result_stream = BytesIO()
    pisa_status = pisa.CreatePDF(StringIO(html), dest=result_stream)

    if pisa_status.err:
        raise Exception("Erro ao gerar PDF com xhtml2pdf")

    with open(caminho_saida, 'wb') as f:
        f.write(result_stream.getvalue())

def salvar_arquivos(resumo, questoes, gabarito, nome_base="material"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_saida = f"output_{timestamp}"
    os.makedirs(pasta_saida, exist_ok=True)

    caminhos = {
        'resumo': os.path.join(pasta_saida, f"{nome_base}_resumo.txt"),
        'questoes': os.path.join(pasta_saida, f"{nome_base}_questoes.txt"),
        'gabarito': os.path.join(pasta_saida, f"{nome_base}_gabarito.txt"),
        'completo': os.path.join(pasta_saida, f"{nome_base}_completo.txt"),
        'pdf': os.path.join(pasta_saida, f"{nome_base}.pdf"),  # Corrigido para incluir o caminho
    }

    with open(caminhos['resumo'], 'w', encoding='utf-8') as f:
        f.write("=== RESUMO DE ESTUDO ===\n\n" + resumo)

    questoes_sem_gabarito = re.sub(r'\s*\(correta\)', '', questoes)
    with open(caminhos['questoes'], 'w', encoding='utf-8') as f:
        f.write("=== QUESTÕES DE ESTUDO ===\n\n" + questoes_sem_gabarito)

    with open(caminhos['gabarito'], 'w', encoding='utf-8') as f:
        f.write("=== GABARITO ===\n\n" + "\n".join(gabarito))

    with open(caminhos['completo'], 'w', encoding='utf-8') as f:
        f.write("=== MATERIAL COMPLETO ===\n\n")
        f.write("RESUMO:\n\n" + resumo)
        f.write("\n\nQUESTÕES:\n\n" + questoes)
        f.write("\n\nGABARITO:\n\n" + "\n".join(gabarito))

    # Corrigir a geração do PDF
    questoes_formatadas_html = formatar_questoes_para_html(questoes)
    html_final = gerar_html(resumo, questoes_formatadas_html, gabarito, nome_base)
    
    # Salvar o PDF no caminho correto (usando caminhos['pdf'])
    with open(caminhos['pdf'], 'wb') as f:
        pisa.CreatePDF(html_final, dest=f, encoding='utf-8')

    return caminhos, pasta_saida


def main():
    print("=== Gerador de Material de Estudo ===")
    print("(Ctrl+C para cancelar a qualquer momento)\n")
    
    try:
        model = configurar_gemini()
        caminho_pdf = input("Digite o caminho para o arquivo PDF: ").strip()
        if not os.path.exists(caminho_pdf):
            raise FileNotFoundError("Arquivo PDF não encontrado!")

        nome_base = os.path.splitext(os.path.basename(caminho_pdf))[0]

        print("\n📄 Extraindo texto do PDF...")
        texto = extrair_texto_pdf(caminho_pdf)
        if not texto.strip():
            raise ValueError("Não foi possível extrair texto do PDF (pode estar em formato de imagem).")

        print("📚 Gerando resumo...")
        resumo = gerar_resumo_gemini(model, texto)

        print("📝 Criando questões...")
        questoes = gerar_questoes_gemini(model, resumo)

        print("✅ Processando gabarito...")
        gabarito = processar_gabarito(questoes)
        questoes_sem_gabarito = re.sub(r'\s*\(correta\)', '', questoes)

        caminhos, pasta = salvar_arquivos(resumo, questoes_sem_gabarito, gabarito, nome_base)

        print(f"\n✅ Material salvo na pasta: {pasta}/")
        print(f"- Resumo: {len(resumo.split())} palavras")
        print(f"- Questões: {len(gabarito)} com gabarito")

        print("\n🔍 Prévia do gabarito:")
        print("\n".join(gabarito[:5]) + ("\n..." if len(gabarito) > 5 else ""))

    except KeyboardInterrupt:
        print("\nOperação cancelada.")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()