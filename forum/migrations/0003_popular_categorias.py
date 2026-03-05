from django.db import migrations

def criar_categorias_iniciais(apps, schema_editor):
    Categoria = apps.get_model('forum', 'Categoria')
    
    categorias = [
        {'nome': '🗣️ Desabafo / Relato', 'slug': 'desabafo-relato', 'descricao': 'Espaço para compartilhar vivências.'},
        {'nome': '♿ Acessibilidade Real', 'slug': 'acessibilidade-real', 'descricao': 'Onde as coisas funcionam (ou não).'},
        {'nome': '📚 Educação e Conceitos', 'slug': 'educacao-conceitos', 'descricao': 'Teoria e leis anticapacitistas.'},
        {'nome': '🎨 Cultura e Mídia', 'slug': 'cultura-midia', 'descricao': 'Representatividade em filmes, livros e artes.'},
        {'nome': '💼 Carreira e Estudos', 'slug': 'carreira-estudos', 'descricao': 'Inclusão no mercado e na academia.'},
        {'nome': '🤝 Rede de Apoio', 'slug': 'rede-apoio', 'descricao': 'Dicas para aliados e familiares.'},
        {'nome': '✨ Conquistas', 'slug': 'conquistas', 'descricao': 'Vitórias da comunidade PCD.'},
        {'nome': '❓ Outro', 'slug': 'outro', 'descricao': 'Assuntos que não se encaixam nas outras categorias.'},
    ]

    for cat in categorias:
        Categoria.objects.get_or_create(
            slug=cat['slug'], 
            defaults={'nome': cat['nome'], 'descricao': cat['descricao']}
        )

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(criar_categorias_iniciais),
    ]