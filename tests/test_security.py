"""
Testes de anonimização — os mais críticos do sistema.

Regra de ouro: user_id NUNCA pode ser recuperado a partir do token.
Esses testes garantem as três propriedades fundamentais da anonimização.
"""

from app.core.security import generate_anon_token


def test_anon_token_nao_contem_user_id():
    """Token não pode conter o user_id — anonimização irreversível."""
    user_id = "usuario-identificavel-123"
    token = generate_anon_token(user_id=user_id, workspace_salt="salt-qualquer")
    assert user_id not in token


def test_mesmo_usuario_mesmo_workspace_gera_mesmo_token():
    """
    Propriedade de idempotência: mesmo input → mesmo output.
    Isso permite detectar resposta duplicada sem saber quem é o usuário.
    """
    token1 = generate_anon_token("user-abc", "workspace-salt-xyz")
    token2 = generate_anon_token("user-abc", "workspace-salt-xyz")
    assert token1 == token2


def test_mesmo_usuario_workspaces_diferentes_geram_tokens_diferentes():
    """
    Isolamento entre workspaces: o mesmo usuário em empresas diferentes
    não pode ser rastreado entre elas.
    """
    token_empresa_a = generate_anon_token("user-abc", "salt-empresa-a")
    token_empresa_b = generate_anon_token("user-abc", "salt-empresa-b")
    assert token_empresa_a != token_empresa_b


def test_usuarios_diferentes_mesmo_workspace_geram_tokens_diferentes():
    """Dois usuários distintos nunca compartilham o mesmo token."""
    token_user1 = generate_anon_token("user-001", "workspace-salt")
    token_user2 = generate_anon_token("user-002", "workspace-salt")
    assert token_user1 != token_user2


def test_token_tem_tamanho_fixo():
    """Token HMAC-SHA256 sempre tem 64 caracteres hexadecimais."""
    token = generate_anon_token("qualquer-id", "qualquer-salt")
    assert len(token) == 64


def test_token_nao_contem_salt():
    """Salt do workspace também não pode vazar no token."""
    salt = "salt-super-secreto-da-empresa"
    token = generate_anon_token("user-123", salt)
    assert salt not in token
