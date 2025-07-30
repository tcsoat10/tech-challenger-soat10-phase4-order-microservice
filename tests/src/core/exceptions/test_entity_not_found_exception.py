
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.base_exception import BaseDomainException

def test_entity_not_found_exception():
    exception: BaseDomainException = EntityNotFoundException(entity_name="TestEntity", id="12345")

    assert exception.detail['message'] == "TestEntity not found."
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {"id": "12345"}

def test_entity_not_found_exception_without_entity_name():
    exception: BaseDomainException = EntityNotFoundException(id="12345")

    assert exception.detail['message'] == "Entity not found."
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {"id": "12345"}

def test_entity_not_found_exception_with_custom_message():
    exception: BaseDomainException = EntityNotFoundException(message="Custom not found message", id="12345")

    assert exception.detail['message'] == "Custom not found message"
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {"id": "12345"}
    
def test_no_entity_name_or_message():
    exception: BaseDomainException = EntityNotFoundException()

    assert exception.detail['message'] == "Entity not found."
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {}
    
def test_none_entity_name():
    exception: BaseDomainException = EntityNotFoundException(entity_name=None, id="12345")

    assert exception.detail['message'] == "Entity not found."
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {"id": "12345"}
    
def test_entity_not_found_exception_with_additional_details():
    exception: BaseDomainException = EntityNotFoundException(entity_name="TestEntity", id="12345", additional_info="Extra details")

    assert exception.detail['message'] == "TestEntity not found."
    assert exception.detail['code'] == "ENTITY_NOT_FOUND"
    assert exception.detail['details'] == {"id": "12345", "additional_info": "Extra details"}
