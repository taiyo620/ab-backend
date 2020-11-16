from django.conf import settings
import matplotlib.pyplot as plt
import japanize_matplotlib
import os
from .models import Graphs

def make_pi(series,file_name):
    Graphs.objects.all().delete()
    colors = ["#2dedc7","#B3FB30","#EF2D56","#FF8230","#0EA486","#7CBD03","#A50D2E","#C64C00"]
    series.plot(fontsize=13,ylabel="",kind="pie",startangle=90,wedgeprops={'linewidth':3,'edgecolor':'white'},counterclock=False,colors=colors)
    image_url = os.path.join(settings.MEDIA_ROOT,file_name)
    plt.savefig(image_url)
    pi_graph = Graphs()
    im = open(image_url,"rb")
    pi_graph.graph.save(file_name,im,save=True)
    im.close()
    plt.clf()
    plt.close()
    return pi_graph
