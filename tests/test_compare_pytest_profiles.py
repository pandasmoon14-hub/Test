import xml.etree.ElementTree as ET

import pytest

from scripts.compare_pytest_profiles import compare, profile


def report(tmp_path, name, cases):
    root = ET.Element('testsuites')
    suite = ET.SubElement(root, 'testsuite', time='2')
    for identity, status in cases:
        case = ET.SubElement(suite, 'testcase', classname='tests.example', name=identity, time='1')
        if status:
            ET.SubElement(case, status, type='pytest.xfail' if status == 'skipped' else status)
    path = tmp_path / name
    ET.ElementTree(root).write(path)
    return path


def test_order_independent_but_missing_extra_and_changed_outcome_fail(tmp_path):
    a = report(tmp_path, 'a.xml', [('one', None), ('two', 'skipped')])
    b = report(tmp_path, 'b.xml', [('two', 'skipped'), ('one', None)])
    assert compare(a, b)['equivalent']
    for cases in ([('one', None)], [('one', None), ('two', None)],
                  [('one', None), ('two', 'skipped'), ('extra', None)]):
        assert not compare(a, report(tmp_path, 'b.xml', cases))['equivalent']


@pytest.mark.parametrize('cases', [[], [('one', None), ('one', None)],
                                   [('one', 'failure')], [('one', 'error')]])
def test_empty_duplicate_and_unsuccessful_reports_rejected(tmp_path, cases):
    with pytest.raises(ValueError):
        profile(report(tmp_path, 'bad.xml', cases))


def test_collection_error_summary_cannot_pass_with_matching_testcases(tmp_path):
    path = report(tmp_path, 'collection.xml', [('one', None)])
    tree = ET.parse(path)
    tree.getroot().find('testsuite').set('errors', '1')
    tree.write(path)
    with pytest.raises(ValueError, match='collection errors'):
        profile(path)


def test_xfail_and_ordinary_skip_are_not_equivalent(tmp_path):
    a = report(tmp_path, 'xfail.xml', [('one', 'skipped')])
    b = report(tmp_path, 'skip.xml', [('one', 'skipped')])
    tree = ET.parse(b)
    tree.getroot().find('.//skipped').set('type', 'pytest.skip')
    tree.write(b)
    assert not compare(a, b)['equivalent']
