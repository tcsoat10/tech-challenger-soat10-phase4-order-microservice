from src.constants import messages

def test_product_not_found_message():
    assert messages.PRODUCT_NOT_FOUND == "Produto não encontrado"

def test_category_not_found_message():
    assert messages.CATEGORY_NOT_FOUND == "Categoria não encontrada"
