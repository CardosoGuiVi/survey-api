import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, Workspace, WorkspaceUser
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:100]


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def register(self, data: RegisterRequest) -> TokenResponse:
        # Verifica e-mail duplicado
        existing = await self.db.scalar(select(User).where(User.email == data.email))
        if existing:
            raise ValueError("E-mail já cadastrado")

        # Cria usuário
        user = User(
            email=data.email,
            name=data.name,
            password_hash=hash_password(data.password),
        )
        self.db.add(user)

        # Cria workspace com slug único
        base_slug = slugify(data.workspace_name)
        slug = await self._unique_slug(base_slug)

        workspace = Workspace(name=data.workspace_name, slug=slug)
        self.db.add(workspace)

        # Associa usuário como admin do workspace
        membership = WorkspaceUser(
            workspace=workspace,
            user=user,
            role="admin",
        )
        self.db.add(membership)

        await self.db.commit()
        await self.db.refresh(user)
        await self.db.refresh(workspace)

        return self._build_token(user, workspace, role="admin")

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.db.scalar(select(User).where(User.email == data.email))
        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Credenciais inválidas")

        # Pega primeiro workspace ativo do usuário
        membership = await self.db.scalar(
            select(WorkspaceUser).where(
                WorkspaceUser.user_id == user.id,
                WorkspaceUser.is_active == True,  # noqa: E712
            )
        )
        if not membership:
            raise ValueError("Usuário sem workspace ativo")

        workspace = await self.db.get(Workspace, membership.workspace_id)
        if not workspace:
            raise ValueError("Workspace não encontrado")

        return self._build_token(user, workspace, role=membership.role)

    def _build_token(
        self, user: User, workspace: Workspace, role: str
    ) -> TokenResponse:
        token = create_access_token(
            {
                "user_id": str(user.id),
                "workspace_id": str(workspace.id),
                "role": role,
            }
        )
        return TokenResponse(access_token=token)

    async def _unique_slug(self, base: str) -> str:
        slug = base
        counter = 1
        while await self.db.scalar(select(Workspace).where(Workspace.slug == slug)):
            slug = f"{base}-{counter}"
            counter += 1
        return slug
