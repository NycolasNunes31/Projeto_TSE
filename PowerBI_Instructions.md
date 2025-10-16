# Modelo Power BI — Estrutura e Medidas (Versão Desktop)

Este pacote contém templates CSV (em branco) e instruções para montar o relatório **Power BI Desktop** conforme solicitado:
- Estilo: **Profissional e limpo**
- Tema: **Modo claro**
- Conteúdo: **Estrutura de tabelas** e **medidas DAX** (sem dados simulados)

## Conteúdo do ZIP
- `Eleicao_template.csv` — Cabeçalhos: Ano, UF, Municipio, Candidato, Partido, Votos, Total_Eleitores
- `Demografia_template.csv` — Cabeçalhos: Municipio, Populacao, Renda_Media, Escolaridade_Media
- `Engajamento_template.csv` — Cabeçalhos: Candidato, Municipio, Indice_Engajamento
- `PowerBI_Instructions.md` — Este arquivo (instruções detalhadas)
- `Theme_Light.json` — Tema claro sugerido para usar no Power BI

---

## Passo a passo rápido (Power BI Desktop)

1. Abra o **Power BI Desktop** (Windows).
2. Clique em **Obter dados > Texto/CSV** e importe os três arquivos CSV.
3. No Editor de Consultas (Power Query):
   - Verifique tipos de dados:
     - `Ano` → Inteiro
     - `Votos`, `Total_Eleitores`, `Populacao`, `Renda_Media`, `Escolaridade_Media`, `Indice_Engajamento` → Decimal/Inteiro conforme desejar
   - Remova linhas em branco, padronize nomes de municípios e partidos.
   - Carregue os dados.

4. No **Model** (Modelagem):
   - Crie relacionamentos:
     - `Eleicao[Municipio] (N)` → `Demografia[Municipio] (1)`
     - `Eleicao[Municipio] (N)` → `Engajamento[Municipio] (1)`
     - `Eleicao[Candidato] (N)` → `Engajamento[Candidato] (1)`
   - Direção: Single (das tabelas Demografia/Engajamento para Eleicao).

5. Medidas DAX (crie na tabela `Eleicao` ou numa tabela de medidas):
   - **Total_Votos**
   ```DAX
   Total_Votos = SUM(Eleicao[Votos])
   ```
   - **Percentual_Votos**
   ```DAX
   Percentual_Votos = DIVIDE(SUM(Eleicao[Votos]), SUM(Eleicao[Total_Eleitores]), 0)
   ```
   - **Crescimento_Votos**
   ```DAX
   Crescimento_Votos = 
   VAR VotosAtual = SUM(Eleicao[Votos])
   VAR VotosAnterior = CALCULATE(SUM(Eleicao[Votos]), PREVIOUSYEAR(Eleicao[Ano]))
   RETURN DIVIDE(VotosAtual - VotosAnterior, VotosAnterior, 0)
   ```
   - **Taxa_Abstencao**
   ```DAX
   Taxa_Abstencao = 1 - [Percentual_Votos]
   ```
   - **Previsao_Votos**
   ```DAX
   Previsao_Votos = 
   VAR Media_Renda = AVERAGE(Demografia[Renda_Media])
   VAR Media_Escolaridade = AVERAGE(Demografia[Escolaridade_Media])
   VAR Media_Engajamento = AVERAGE(Engajamento[Indice_Engajamento])
   RETURN (Media_Renda * 0.4 + Media_Escolaridade * 0.3 + Media_Engajamento * 0.3)
   ```
   - **Desempenho_Previsto**
   ```DAX
   Desempenho_Previsto = DIVIDE([Total_Votos] - [Previsao_Votos], [Previsao_Votos], 0)
   ```

6. Páginas sugeridas:
   - **Base de Dados**: tabelas e slicers (Ano, UF, Partido, Candidato)
   - **Análise Descritiva**: gráficos — linha (votos ao longo do tempo), barras (votos por partido), mapa coroplético (votos por município), KPIs
   - **Análise Preditiva**: gráfico de linha com série histórica + linha de previsão (use "Análise → Previsão" no visual ou mostre [Previsao_Votos]), tabela comparativa Real x Previsto, indicador de desvio
   - **Dashboard Político**: KPIs principais + mapa e top N municípios

7. Tema (modo claro):
   - Importe o arquivo `Theme_Light.json` no Power BI: **Exibir > Temas > Importar tema**.
   - O tema inclui tipografia e paleta de cores neutras (azul, cinza, branco).

---

## Dicas extras
- Para previsões mais robustas, conecte séries temporais de pesquisas de intenção de voto e use R/Python (script visuals) ou Azure ML.
- Configure atualização agendada ao publicar no Power BI Service (se desejar).
- Padronize nomes de municípios (sem acentos, ou usando um código IBGE) para evitar problemas de relacionamento.

---

Se quiser, eu também posso:
- Gerar um `.pbix` com a estrutura pronta (não consigo criar diretamente aqui, mas posso orientar passo a passo para montar em ~10 minutos).
- Ajudar a conectar com APIs (TSE/IBGE) e preparar consultas Power Query prontas.

