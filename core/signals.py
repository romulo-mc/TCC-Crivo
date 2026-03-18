from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from forum.models import Topico, Resposta
from library.models import LibraryItem, Review
from .models import Notificacao

@receiver(post_save, sender=Resposta)
def notificar_interacao_forum(sender, instance, created, **kwargs):
    if created and instance.status == 'APROVADO':
        topico = instance.topico
        autor_atual = instance.autor
        link = reverse('detalhe_topico', kwargs={'slug': topico.slug})
        dono_topico = topico.autor
        if dono_topico and autor_atual != dono_topico:
            Notificacao.objects.create(
                destinatario=dono_topico,
                tipo='RESPOSTA',
                mensagem=f"{autor_atual.username} comentou no seu tópico: '{topico.titulo}'",
                link=link
            )
        if instance.pai:
            dono_comentario_pai = instance.pai.autor
            if dono_comentario_pai and \
               autor_atual != dono_comentario_pai and \
               dono_comentario_pai != dono_topico:
                
                Notificacao.objects.create(
                    destinatario=dono_comentario_pai,
                    tipo='RESPOSTA',
                    mensagem=f"{autor_atual.username} respondeu ao seu comentário no tópico '{topico.titulo}'",
                    link=link
                )

@receiver(post_save, sender=Review)
def notificar_nova_review(sender, instance, created, **kwargs):
    if created:
        destinatario = instance.item.usuario_criador
        if destinatario and instance.user != destinatario:
            link = reverse('detalhe_item', kwargs={'id': instance.item.id})
            Notificacao.objects.create(
                destinatario=destinatario,
                tipo='AVALIACAO',
                mensagem=f"{instance.user.username} avaliou a obra que você cadastrou: '{instance.item.titulo}'",
                link=link
            )



@receiver(pre_save, sender=Topico)
def notificar_moderacao_topico(sender, instance, **kwargs):
    if instance.id:
        try:
            antigo = Topico.objects.get(id=instance.id)
        except Topico.DoesNotExist: return

        if antigo.status != 'REJEITADO' and instance.status == 'REJEITADO':
            motivo = f" Motivo: {instance.motivo_rejeicao}" if instance.motivo_rejeicao else ""
            Notificacao.objects.create(
                destinatario=instance.autor,
                tipo='MODERACAO',
                mensagem=f"Seu tópico '{instance.titulo}' foi rejeitado.{motivo}",
                link="#"
            )
        elif antigo.status != 'APROVADO' and instance.status == 'APROVADO':
            Notificacao.objects.create(
                destinatario=instance.autor,
                tipo='MODERACAO',
                mensagem=f"Seu tópico '{instance.titulo}' foi aprovado! 🎉",
                link=reverse('detalhe_topico', kwargs={'slug': instance.slug})
            )

@receiver(pre_save, sender=LibraryItem)
def notificar_moderacao_library(sender, instance, **kwargs):
    if instance.id:
        try:
            antigo = LibraryItem.objects.get(id=instance.id)
        except LibraryItem.DoesNotExist: return

        if antigo.status != 'REJEITADO' and instance.status == 'REJEITADO':
            motivo = f" Motivo: {instance.motivo_rejeicao}" if instance.motivo_rejeicao else ""
            Notificacao.objects.create(
                destinatario=instance.usuario_criador,
                tipo='MODERACAO',
                mensagem=f"A obra '{instance.titulo}' que você sugeriu foi rejeitada.{motivo}",
                link="#"
            )
        elif antigo.status != 'ATIVO' and instance.status == 'ATIVO':
            Notificacao.objects.create(
                destinatario=instance.usuario_criador,
                tipo='MODERACAO',
                mensagem=f"A obra '{instance.titulo}' foi aprovada! 🎉",
                link=reverse('detalhe_item', kwargs={'id': instance.id})
            )