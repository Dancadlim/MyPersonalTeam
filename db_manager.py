import sqlite3
import json

DB_NAME = "meu_time.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tabela de Usuários
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE,
                    dados_json TEXT
                )''')
    
    # Tabela de Planos
    c.execute('''CREATE TABLE IF NOT EXISTS planos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER,
                    plano_texto TEXT,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
                )''')
    
    conn.commit()
    conn.close()

def salvar_usuario(dados):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    nome = dados.get('nome')
    dados_json = json.dumps(dados)
    
    try:
        # Tenta inserir, se já existe atualiza
        c.execute("INSERT OR REPLACE INTO usuarios (nome, dados_json) VALUES (?, ?)", (nome, dados_json))
        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar usuario: {e}")
    finally:
        conn.close()

def buscar_usuario(nome):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, dados_json FROM usuarios WHERE nome = ?", (nome,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return result[0], json.loads(result[1])
    return None, None

def listar_usuarios():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT nome FROM usuarios")
    usuarios = [row[0] for row in c.fetchall()]
    conn.close()
    return usuarios

def salvar_plano(usuario_id, plano_texto):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO planos (usuario_id, plano_texto) VALUES (?, ?)", (usuario_id, plano_texto))
    conn.commit()
    conn.close()

def ler_plano_recente(usuario_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT plano_texto FROM planos WHERE usuario_id = ? ORDER BY id DESC LIMIT 1", (usuario_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
