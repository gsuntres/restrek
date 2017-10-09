from restrek.parsing import yaml_load


def test_load():
    output = yaml_load("{'foo': 'bar'}")
    assert {'foo': 'bar'} == output
