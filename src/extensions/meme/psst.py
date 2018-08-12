psst_txt = """
┳┻|
┻┳|
┳┻|  psst! hey kid!
┻┳|
┳┻|
┻┳|
┳┻|
┻┳|
┳┻|
┻┳|
┳┻|
┻┳|
┳┻| _
┻┳| •.•)  {0}
┳┻|⊂ﾉ {1}
┻┳|       {2}
┳┻|       {3}
┻┳|       {4}
┳┻|
"""


def split_txt(txt, num_segments):
    words = txt.split(' ')
    step = len(words) // num_segments
    ls = []
    for i in range(num_segments):
        line = ' '.join(words.pop(0) for _ in range(step))
        ls.append(line)

    if words:
        ls[-1] += ' ' + ' '.join(words)

    return ls


def format_psst(txt):
    return psst_txt.format(*split_txt(txt, 5))
