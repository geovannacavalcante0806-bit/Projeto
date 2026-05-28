README Resumido
Sistema de Gerenciamento de Estoque
Sistema Python para controlar estoque com cadastro, movimentações, consultas, alertas e relatórios.

📁 Arquivos
text
main.py                      # Menu principal
conexao_banco.py             # Inicializa banco SQLite
modulo_cadastro.py           # Módulo 1: Cadastro de produtos
modulo_movimentacao.py       # Módulo 2: Entrada/saída de estoque
modulo_consulta.py           # Módulo 3: Listar produtos e histórico
modulo_alertas_relatorios.py # Módulo 4: Alertas e relatórios
🚀 Como Executar
bash
python main.py
Todos os arquivos devem estar na mesma pasta. O banco banco.db é criado automaticamente.

📖 Menu
text
1. Cadastrar produto
2. Listar produtos
3. Registrar movimentação de estoque
4. Mostrar histórico de movimentações
5. Alertas inteligentes
6. Relatório gerencial
7. Sair
🔧 Módulos
Módulo	Arquivo	Função
1	modulo_cadastro.py	cadastrar_produto()
2	modulo_movimentacao.py	registrar_movimentacao()
3	modulo_consulta.py	listar_produtos(), mostrar_movimentacoes()
4	modulo_alertas_relatorios.py	alertas_inteligentes(), relatorio_gerencial()
🗄️ Banco de Dados
Tabelas:

produtos: código, nome, categoria, quantidade, unidade, preço, estoque mínimo, especificações

movimentacoes: id, produto_id, tipo (entrada/saida), motivo, quantidade, data

⚙️ Tecnologias
Python 3.x

sqlite3 (banco de dados)

os (verificação de arquivos)

⚠️ Importantes
Valida estoque para saídas

Alerta quando quantidade <= estoque_minimo

Relatório mostra: total de itens, valor total, produtos com estoque baixo
