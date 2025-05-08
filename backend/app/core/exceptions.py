class AuthenticationError(Exception):
    """Exceção lançada quando há erro na autenticação"""

    pass


class BusinessError(Exception):
    """Exceção base para erros de negócio"""

    pass


class ValidationError(BusinessError):
    """Exceção lançada quando há erro de validação"""

    pass


class NotFoundError(BusinessError):
    """Exceção lançada quando um recurso não é encontrado"""

    pass


class DuplicateError(BusinessError):
    """Exceção lançada quando tenta-se criar um recurso duplicado"""

    pass


class UnauthorizedError(BusinessError):
    """Exceção lançada quando o usuário não tem permissão"""

    pass
