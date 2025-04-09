# T.I.A.
### ✨ Funcionalidades

- 📄 Extração de texto de PDFs
- 📚 Geração de resumos acadêmicos
- 📝 Criação de 10 questões de múltipla escolha com alternativas plausíveis
- ✅ Gabarito gerado automaticamente
- 💾 Exporta tudo em arquivos `.txt` organizados por pasta com data/hora

### ⚙️ Como usar

1. Certifique-se de ter um arquivo `.env` com sua chave de API:

2. Instale as dependências:
```bash
pip install xhtml2pdf PyPDF2 markdown2 google-generativeai python-dotenv
```
Rode o script principal:
```bash
python tiagemini.py
```

Insira o caminho para o PDF quando solicitado.

### 📁 Estrutura dos arquivos gerados
Ao final, será criada uma pasta com os seguintes arquivos:

- material_resumo.pdf

- material_resumo.txt

- material_questoes.txt

- material_gabarito.txt

- material_completo.txt

### 📌 Requisitos
- Python 3.10+

- API Key válida do Google Gemini

- Biblioteca google-generativeai

- Biblioteca PyPDF2

- Biblioteca python-dotenv

- Biblioteca xhtml12pdf

- Biblioteca markdown2
