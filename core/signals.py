from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from forum.models import Topico, Resposta
from library.models import LibraryItem, Review
from .models import Notificacao

def obter_link_completo(caminho):
    base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    
    if base_url.endswith('/'):
        base_url = base_url[:-1]
        
    return f"{base_url}{caminho}"

def disparar_email_notificacao(usuario, assunto, mensagem_html):
    if hasattr(usuario, 'profile') and usuario.profile.receber_notificacoes:
        mensagem_texto = strip_tags(mensagem_html)
        try:
            send_mail(
                subject=assunto,
                message=mensagem_texto,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[usuario.email],
                html_message=mensagem_html,
                fail_silently=True,
            )
        except Exception:
            pass

@receiver(post_save, sender=Resposta)
def notificar_interacao_forum(sender, instance, created, **kwargs):
    if created and instance.status == 'APROVADO':
        topico = instance.topico
        autor_atual = instance.autor
        link = reverse('detalhe_topico', kwargs={'slug': topico.slug})
        dono_topico = topico.autor
        
        if dono_topico and autor_atual != dono_topico:
            msg = f"{autor_atual.username} comentou no seu tópico: '{topico.titulo}'"
            Notificacao.objects.create(
                destinatario=dono_topico, tipo='RESPOSTA', mensagem=msg, link=link
            )
            html_email = f"<h3>Novo comentário no Crivo!</h3><p>{msg}</p><p><a href='{obter_link_completo(link)}'>Clique aqui para ver</a></p>"
            disparar_email_notificacao(dono_topico, "[Crivo] Novo comentário no seu tópico", html_email)

        if instance.pai:
            dono_comentario_pai = instance.pai.autor
            if dono_comentario_pai and autor_atual != dono_comentario_pai and dono_comentario_pai != dono_topico:
                msg_resp = f"{autor_atual.username} respondeu ao seu comentário no tópico '{topico.titulo}'"
                Notificacao.objects.create(
                    destinatario=dono_comentario_pai, tipo='RESPOSTA', mensagem=msg_resp, link=link
                )
                html_email_resp = f"<h3>Nova resposta no Crivo!</h3><p>{msg_resp}</p><p><a href='{obter_link_completo(link)}'>Clique aqui para ver</a></p>"
                disparar_email_notificacao(dono_comentario_pai, "[Crivo] Responderam seu comentário", html_email_resp)

@receiver(post_save, sender=Review)
def notificar_nova_review(sender, instance, created, **kwargs):
    if created:
        destinatario = instance.item.usuario_criador
        if destinatario and instance.user != destinatario:
            link = reverse('detalhe_item', kwargs={'id': instance.item.id})
            msg = f"{instance.user.username} avaliou a obra que você cadastrou: '{instance.item.titulo}'"
            Notificacao.objects.create(
                destinatario=destinatario, tipo='AVALIACAO', mensagem=msg, link=link
            )
            html_email = f"<h3>Nova avaliação no Crivo!</h3><p>{msg}</p><p><a href='{obter_link_completo(link)}'>Clique aqui para ver a obra</a></p>"
            disparar_email_notificacao(destinatario, "[Crivo] Nova avaliação na sua indicação", html_email)

@receiver(pre_save, sender=Topico)
def notificar_moderacao_topico(sender, instance, **kwargs):
    if instance.id:
        try:
            antigo = Topico.objects.get(id=instance.id)
        except Topico.DoesNotExist: return

        if antigo.status != 'REJEITADO' and instance.status == 'REJEITADO':
            motivo = f" Motivo: {instance.motivo_rejeicao}" if instance.motivo_rejeicao else ""
            msg = f"Seu tópico '{instance.titulo}' foi rejeitado.{motivo}"
            Notificacao.objects.create(
                destinatario=instance.autor, tipo='MODERACAO', mensagem=msg, link="#"
            )
            html_email = f"<h3>Aviso da Moderação</h3><p>{msg}</p>"
            disparar_email_notificacao(instance.autor, "[Crivo] Atualização sobre o seu tópico", html_email)
            
        elif antigo.status != 'APROVADO' and instance.status == 'APROVADO':
            msg = f"Seu tópico '{instance.titulo}' foi aprovado! 🎉"
            link = reverse('detalhe_topico', kwargs={'slug': instance.slug})
            Notificacao.objects.create(
                destinatario=instance.autor, tipo='MODERACAO', mensagem=msg, link=link
            )
            html_email = f"<h3>Boas notícias!</h3><p>{msg}</p><p><a href='{obter_link_completo(link)}'>Clique aqui para ver o tópico publicado</a></p>"
            disparar_email_notificacao(instance.autor, "[Crivo] Seu tópico foi aprovado!", html_email)

@receiver(pre_save, sender=LibraryItem)
def notificar_moderacao_library(sender, instance, **kwargs):
    if instance.id:
        try:
            antigo = LibraryItem.objects.get(id=instance.id)
        except LibraryItem.DoesNotExist: return

        if antigo.status != 'REJEITADO' and instance.status == 'REJEITADO':
            motivo = f" Motivo: {instance.motivo_rejeicao}" if instance.motivo_rejeicao else ""
            msg = f"A obra '{instance.titulo}' que você sugeriu foi rejeitada.{motivo}"
            Notificacao.objects.create(
                destinatario=instance.usuario_criador, tipo='MODERACAO', mensagem=msg, link="#"
            )
            html_email = f"<h3>Aviso da Moderação</h3><p>{msg}</p>"
            disparar_email_notificacao(instance.usuario_criador, "[Crivo] Atualização sobre sua indicação", html_email)
            
        elif antigo.status != 'ATIVO' and instance.status == 'ATIVO':
            msg = f"A obra '{instance.titulo}' foi aprovada! 🎉"
            link = reverse('detalhe_item', kwargs={'id': instance.id})
            Notificacao.objects.create(
                destinatario=instance.usuario_criador, tipo='MODERACAO', mensagem=msg, link=link
            )
            html_email = f"<h3>Boas notícias!</h3><p>{msg}</p><p><a href='{obter_link_completo(link)}'>Clique aqui para ver no acervo</a></p>"
            disparar_email_notificacao(instance.usuario_criador, "[Crivo] Sua indicação foi aprovada!", html_email)