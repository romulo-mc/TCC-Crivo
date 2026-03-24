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

def preferencias_usuario(request):
    prefs = {
        'modo_escuro': False,
        'alto_contraste': False,
        'fonte_dislexia': False,
        'fonte_tdah': False,
        'tamanho_fonte': 'M',
        'reduzir_animacoes': False,
    }

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            prefs.update({
                'modo_escuro': profile.modo_escuro,
                'alto_contraste': profile.alto_contraste,
                'fonte_dislexia': profile.fonte_dislexia,
                'fonte_tdah': profile.fonte_tdah,
                'tamanho_fonte': profile.tamanho_fonte,
                'reduzir_animacoes': profile.reduzir_animacoes,
            })
        except Exception:
            pass
    else:
        session_prefs = request.session.get('acessibilidade', {})
        prefs.update(session_prefs)

    return {'user_prefs': prefs}