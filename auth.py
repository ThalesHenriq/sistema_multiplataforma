import hashlib
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    senha_hash: str
    tipo: str
    data_criacao: str
    ultimo_acesso: Optional[str] = None

class GerenciadorUsuarios:
    def __init__(self, arquivo_usuarios="usuarios.json"):
        self.arquivo_usuarios = arquivo_usuarios
        self.carregar_usuarios()
        
        if not self.usuarios:
            self.criar_admin_padrao()
    
    def carregar_usuarios(self):
        if os.path.exists(self.arquivo_usuarios):
            with open(self.arquivo_usuarios, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.usuarios = [Usuario(**u) for u in dados]
        else:
            self.usuarios = []
    
    def salvar_usuarios(self):
        with open(self.arquivo_usuarios, 'w', encoding='utf-8') as f:
            dados = [u.__dict__ for u in self.usuarios]
            json.dump(dados, f, indent=4, ensure_ascii=False)
    
    def criar_admin_padrao(self):
        senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
        admin = Usuario(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            nome="Administrador",
            email="admin@sistema.com",
            senha_hash=senha_hash,
            tipo="admin",
            data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.usuarios.append(admin)
        self.salvar_usuarios()
    
    def autenticar(self, email: str, senha: str) -> Optional[Usuario]:
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha_hash == senha_hash:
                usuario.ultimo_acesso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.salvar_usuarios()
                return usuario
        return None
    
    def criar_usuario(self, nome: str, email: str, senha: str) -> tuple:
        if any(u.email == email for u in self.usuarios):
            return False, "Email já cadastrado"
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        novo_usuario = Usuario(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo="usuario",
            data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()
        return True, "Usuário criado com sucesso"