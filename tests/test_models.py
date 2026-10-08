from datetime import datetime

from fakepinterest.models import Foto, Usuario


def test_usuario_criado_com_sucesso(sessao):
    usuario = Usuario(username="ana", email="ana@exemplo.com", senha="hash")
    sessao.add(usuario)
    sessao.commit()

    assert usuario.id is not None
    assert usuario.username == "ana"


def test_relacionamento_usuario_fotos(sessao):
    usuario = Usuario(username="bia", email="bia@exemplo.com", senha="hash")
    sessao.add(usuario)
    sessao.commit()

    foto = Foto(id_usuario=usuario.id)
    sessao.add(foto)
    sessao.commit()

    assert foto in usuario.fotos
    assert foto.usuario == usuario


def test_foto_imagem_padrao(sessao):
    usuario = Usuario(username="caio", email="caio@exemplo.com", senha="hash")
    sessao.add(usuario)
    sessao.commit()

    foto = Foto(id_usuario=usuario.id)
    sessao.add(foto)
    sessao.commit()

    assert foto.imagem == "default.png"


def test_foto_data_criacao_preenchida(sessao):
    usuario = Usuario(username="duda", email="duda@exemplo.com", senha="hash")
    sessao.add(usuario)
    sessao.commit()

    foto = Foto(id_usuario=usuario.id)
    sessao.add(foto)
    sessao.commit()

    assert isinstance(foto.data_criacao, datetime)
