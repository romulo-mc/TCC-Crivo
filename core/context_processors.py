from .models import Notificacao

def notificacoes_globais(request):
    if request.user.is_authenticated:
        notificacoes = Notificacao.objects.filter(destinatario=request.user)[:10]
        nao_lidas = Notificacao.objects.filter(destinatario=request.user, lida=False).count()
        return {
            'notificacoes_usuario': notificacoes,
            'notificacoes_nao_lidas_count': nao_lidas
        }
    return {}