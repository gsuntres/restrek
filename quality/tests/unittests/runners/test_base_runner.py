import pytest


def test_check_expand_plans(runner):
    plans = runner._expand_plans(['group1.plan1'])
    assert 1 == len(plans)


def test_expand_plans_single_group(runner):
    exp_plans = runner._expand_plans(['group1'])
    assert 3 == len(exp_plans)
    assert 'group1.plan2_1' == exp_plans[0]
    assert 'group1.plan1_1' == exp_plans[1]
    assert 'group1.plan3_1' == exp_plans[2]
