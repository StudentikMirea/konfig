import pytest
from config_parser import ConfigParser

def test_const_declaration():
    parser = ConfigParser()
    content = "const port = 8080"
    result = parser.parse(content)
    assert result == {'port': 8080}

def test_list_declaration():
    parser = ConfigParser()
    content = "(list 127.0.0.1 8080 1000)"
    result = parser.parse(content)
    assert result == {'list': ['127.0.0.1', 8080, 1000]}

def test_constant_reference():
    parser = ConfigParser()
    content = "const port = 8080\n(list 127.0.0.1 !{port})"
    result = parser.parse(content)
    assert result == {'port': 8080, 'list': ['127.0.0.1', 8080]}

def test_full_config():
    parser = ConfigParser()
    content = """
    const port = 8080
    const max_connections = 1000
    (list 127.0.0.1 !{port} !{max_connections})
    """
    result = parser.parse(content)
    assert result == {'port': 8080, 'max_connections': 1000, 'list': ['127.0.0.1', 8080, 1000]}

def test_multiline_comment():
    parser = ConfigParser()
    content = """
    /*
    Это многострочный комментарий
    */
    const port = 8080
    (list 127.0.0.1 !{port})
    """
    result = parser.parse(content)
    assert result == {'port': 8080, 'list': ['127.0.0.1', 8080]}

def test_single_line_comment():
    parser = ConfigParser()
    content = """
    REM Это однострочный комментарий
    const port = 8080
    (list 127.0.0.1 !{port})
    """
    result = parser.parse(content)
    assert result == {'port': 8080, 'list': ['127.0.0.1', 8080]}
