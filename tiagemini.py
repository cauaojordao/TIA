import os
import re
from PyPDF2 import PdfReader
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_NAME = "gemini-1.5-pro"

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

def salvar_arquivos(resumo, questoes, gabarito, nome_base="material"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_saida = f"output_{timestamp}"
    os.makedirs(pasta_saida, exist_ok=True)

    caminhos = {
        'resumo': os.path.join(pasta_saida, f"{nome_base}_resumo.txt"),
        'questoes': os.path.join(pasta_saida, f"{nome_base}_questoes.txt"),
        'gabarito': os.path.join(pasta_saida, f"{nome_base}_gabarito.txt"),
        'completo': os.path.join(pasta_saida, f"{nome_base}_completo.txt")
    }

    with open(caminhos['resumo'], 'w', encoding='utf-8') as f:
        f.write("=== RESUMO DE ESTUDO ===\n\n")
        f.write(resumo)

    questoes_sem_gabarito = re.sub(r'\s*\(correta\)', '', questoes)
    with open(caminhos['questoes'], 'w', encoding='utf-8') as f:
        f.write("=== QUESTÕES DE ESTUDO ===\n\n")
        f.write(questoes_sem_gabarito)

    with open(caminhos['gabarito'], 'w', encoding='utf-8') as f:
        f.write("=== GABARITO ===\n\n")
        f.write("\n".join(gabarito))

    with open(caminhos['completo'], 'w', encoding='utf-8') as f:
        f.write("=== MATERIAL COMPLETO ===\n\n")
        f.write("RESUMO:\n\n")
        f.write(resumo)
        f.write("\n\nQUESTÕES:\n\n")
        f.write(questoes)
        f.write("\n\nGABARITO:\n\n")
        f.write("\n".join(gabarito))

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
