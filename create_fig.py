
import matplotlib.pyplot as plt


def create_fig():
    fig = plt.figure(num=None, figsize=(14.5, 8.5), facecolor='w', edgecolor='k')
    fig.subplots_adjust(left=0.05, bottom=0.04, right=0.96, top=0.98, wspace=0.1, hspace=0.14)
    return fig


def add_subplots(fig, count=1, vertical=True):
    plts = []
    if count == 1:
        plts = [111]
    elif count == 2 and vertical:
        plts = [211, 212]
    elif count == 2 and not vertical:
        plts = [121, 122]
    elif count == 3 and vertical:
        plts = [311, 312, 313]
    elif count == 3 and not vertical:
        plts = [131, 132, 133]
    elif count == 4:
        plts = [221, 222, 223, 224]
    else:
        return None

    return [fig.add_subplot(c) for c in plts]
