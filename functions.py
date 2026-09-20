import html
import pandas as pd


def _esc(x):
    return html.escape(str(x))


def _lines(items, cls, prefix=''):
    if not items:
        return '<p class="none">none</p>'
    return ''.join(f'<p class="line {cls}">{prefix}{_esc(i)}</p>' for i in items)


def create_header(name1, name2, n_add, n_del, n_chg):
    return (
        '<div class="section"><p class="kicker">Comparing</p>'
        f'<p class="line"><span class="k">from</span> {_esc(name1)}  <span class="k">to</span> {_esc(name2)}</p>'
        f'<div class="summary" style="margin-top:12px">'
        f'<span class="add"><b>{n_add}</b> created</span>'
        f'<span class="del"><b>{n_del}</b> deleted</span>'
        f'<span class="chg"><b>{n_chg}</b> changed</span></div></div>'
    )


def create_modules_data(modules1, modules2):
    deleted = sorted(set(modules1) - set(modules2))
    created = sorted(set(modules2) - set(modules1))
    s = '<div class="section"><p class="kicker">01 · Modules</p>'
    s += '<div class="group"><p class="group-title">Created</p>' + _lines(created, 'add', '+ ') + '</div>'
    s += '<div class="group"><p class="group-title">Deleted</p>' + _lines(deleted, 'del', '- ') + '</div>'
    s += '</div>'
    return s, len(created), len(deleted)


def create_line_items_data(d1, d2):
    created = sorted(set(d2) - set(d1))
    deleted = sorted(set(d1) - set(d2))
    common = set(d1).intersection(d2)
    changed = sorted(k for k in common if d1[k]['Formula'] != d2[k]['Formula'])

    s = '<div class="section"><p class="kicker">02 · Line items</p>'

    s += '<div class="group"><p class="group-title">Created</p>'
    if created:
        for k in created:
            s += (f'<p class="line add">+ {_esc(k[0])}.{_esc(k[1])}'
                  f'<br><span class="k">formula</span> {_esc(d2[k]["Formula"])}</p>')
    else:
        s += '<p class="none">none</p>'
    s += '</div>'

    s += '<div class="group"><p class="group-title">Deleted</p>'
    s += _lines([f'{k[0]}.{k[1]}' for k in deleted], 'del', '- ') + '</div>'

    s += '<div class="group"><p class="group-title">Formula changed</p>'
    if changed:
        for k in changed:
            s += (f'<p class="line chg">{_esc(k[0])}.{_esc(k[1])}'
                  f'<br><span class="from">from</span> {_esc(d1[k]["Formula"])}'
                  f'<br><span class="to">to</span>   {_esc(d2[k]["Formula"])}</p>')
    else:
        s += '<p class="none">none</p>'
    s += '</div></div>'
    return s, len(created), len(deleted), len(changed)


def _line_items(df):
    d = {}
    for _, r in df.iterrows():
        if not pd.isna(r['Formula']):
            d[(r['Module Name'], r['Unnamed: 0'])] = {'Formula': r['Formula']}
    return d


def get_diff(file1, file2, name1='before', name2='after'):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    modules1 = [x for x in df1['Module Name'].unique() if not pd.isna(x)]
    modules2 = [x for x in df2['Module Name'].unique() if not pd.isna(x)]

    d1 = _line_items(df1)
    d2 = _line_items(df2)

    mod_html, m_add, m_del = create_modules_data(modules1, modules2)
    li_html, l_add, l_del, l_chg = create_line_items_data(d1, d2)

    return create_header(name1, name2, m_add + l_add, m_del + l_del, l_chg) + mod_html + li_html
