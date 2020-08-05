import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects
import io

_fontprop = fm.FontProperties(fname='lobster.ttf')

PREF_LINE_LEN = 30

def _split_text(text, pref_line_len = PREF_LINE_LEN):
    lines = [[]]
    last_line_len = 0
    for word in text.split(' '):
        if word == '\n' or last_line_len + len(word) > pref_line_len:
            lines.append([])
            last_line_len = 0
        last_line_len += len(word) + 1
        lines[-1].append(word)
    return '\n'.join(' '.join(line).strip() for line in lines)

def lobsterize(input: io.BytesIO, content: str = 'кек)', format: str = None, wide=False):
    img = mpimg.imread(input, format)
    if wide:
        dpi = img.shape[1] / 4 # ширина
    else:
        dpi = min(img.shape[:2]) / 4 # минимум из ширины и высоты
    figsize = img.shape[1] / dpi, img.shape[0] / dpi
    pref_line_len = PREF_LINE_LEN * figsize[0] / 5
    content = _split_text(content, pref_line_len)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(img, cmap='gray')
    offset = 1 - (figsize[0] - 0.2) / figsize[0]
    text = ax.text(0.5, offset, content,
        fontsize=20,
        fontproperties=_fontprop,
        c='white',
        horizontalalignment='center',
        verticalalignment='baseline',
        transform=ax.transAxes)
    text.set_path_effects([path_effects.Stroke(linewidth=4, foreground='#00000018'),
                           path_effects.Stroke(linewidth=3, foreground='#00000020'),
                           path_effects.Stroke(linewidth=2, foreground='#00000020'),
                           path_effects.Stroke(linewidth=1, foreground='#00000030'),
                           path_effects.Normal()])
    with io.BytesIO() as out:
        fig.savefig(out, dpi=dpi, format='jpg')
        plt.close(fig)
        out.seek(0)
        return out.read()
