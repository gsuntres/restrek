import pytest
from jinja2 import TemplateNotFound
from os.path import join
from restrek.parsing.dataloader import FileTemplateLoader


def test_custom_template(ctx):
    loader = FileTemplateLoader(ctx.ws_manager.plans_dir)
    source, path, uptodate = loader.get_source(None, 'group1.plan2_1')
    assert join(ctx.ws_manager.plans_dir, 'group1', 'plan2_1') == path


def test_custom_template_no_group(ctx):
    loader = FileTemplateLoader(ctx.ws_manager.plans_dir)
    with pytest.raises(TemplateNotFound) as e:
        loader.get_source(None, 'plan2_1')
    assert 'no groups provided for' in str(e.value)


def test_custom_template_no_template_found(ctx):
    loader = FileTemplateLoader(ctx.ws_manager.plans_dir)
    with pytest.raises(TemplateNotFound) as e:
        loader.get_source(None, 'group1.plan10_that_doesnt_exist')


def test_load_plan(dataloader):
    plan = dataloader.load_plan('group1.plan1_1')
    assert len(plan) == 2
    assert 'group1.command1_1' == plan[0]['command']
    assert 'group1.command2_1' == plan[1]['command']


def test_load_cmd(dataloader):
    cmds = dataloader.load_cmd('group1.command1_1')
    assert 'Group 1 : Command 1' in cmds['name']
    assert cmds['http'] is not None
