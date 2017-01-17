#!/usr/bin/env python
"""
InterVene: a tool for intersection and visualization of multiple genomic region sets
Created on January 10, 2017
Version: 1.0
@author: <Aziz Khan>aziz.khan@ncmm.uio.no
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pybedtools import BedTool, example_bedtool
#from intervene import list_venn, genomic_venn, pairwise 
import list_venn, genomic_venn, pairwise 
import argparse
import sys
import os

__version__ = '0.1.0'

def create_dir(dir_path):

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except:
            sys.exit( "Output directory (%s) could not be created." % dir_path )
    return dir_path

def venn_ways(options):
    """

    """
    if not options.c:
        return 2
    if not options.d:
        return 3
    if not options.e:
        return 4
    if not options.f:
        return 5
    if options.f:
        return 6


def main():
    #print 'InterVene: a tool for intersection and visualization of multiple genomic region sets'
    #print 'For more details: https://github.com/asntech/intervene'
    
    desc = """
    
    InterVene: a tool for intersection and visualization of multiple genomic region sets.

    For more details: https://github.com/asntech/intervene

    """
    #print desc
    
    parser = argparse.ArgumentParser(usage='intervene <subcommand> [options]', description=desc)
    subparsers = parser.add_subparsers(dest='command',help='List of subcommands')

    #pairwise
    pairwise_parser = subparsers.add_parser('pairwise', usage='intervene pairwise [options]', 
        description='Pairwise intersection and heatmap of N genomic region sets in <BED/GTF/GFF/VCF> format.',
        help='Pairwise intersection and heatmap of N genomic region sets in <BED/GTF/GFF/VCF> format.')
    pairwise_parser.add_argument('-i','--input', nargs="*",
        help='Input BED/GTF/GFF/VCF files. For files in a directory use *.bed')
    
    pairwise_parser.add_argument('--type', choices=('count','frac','jaccard','fisher','reldist'),
        default='frac', help='Report count/fraction of overlaps or statistical relationships. \n'
                       '{frac}-> calculates the fraction of overlap. \n'
                       'jaccard - Calculate the Jaccard statistic. '
                       'reldist - Calculate the distribution of relative distances. '
                       'fisher - Calculate Fisher statistic. '
                       'Default is "%(default)s"')
   
    pairwise_parser.add_argument('--enrichment', action='store_true',
                    help='Run randomizations (default 1000, specify otherwise '
                    'with --iterations) on each pairwise comparison and '
                    'compute the enrichment score as '
                    '(actual intersection count + 1) / (median randomized + 1)'
                    )
    pairwise_parser.add_argument('--genome', help='Required argument if --type=fisher or --enrichment is '
                    'used. Needs to be a string assembly name like "mm9" or "hg19"')
    pairwise_parser.add_argument('--iterations', default=1000, type=int,
                    help='Number of randomizations to perform for enrichement '
                    'scores')
    pairwise_parser.add_argument('-o', '--output', dest='output', 
                  help='Output folder path where plots will store.'
                       'Default is current working directory.')
    pairwise_parser.add_argument('--htype', dest="htype",choices=("color", "pie","circle", "square", "ellipse", "number", "shade"), 
                   default='circle',help='Heatmap plot type. '
                           'Default is "%(default)s"')    
    pairwise_parser.add_argument('--figtype', dest="figtype",choices=('pdf','svg','png'), 
                   default='pdf',help='Figure type for the plot. '
                       'e.g. --figtype svg. Default is "%(default)s"')    
    pairwise_parser.add_argument('--figsize', default=(8,10),
                   help='Figure size for the output plot. '
                       'e.g. --figsize=8,10 Default is "%(default)s"')    
    pairwise_parser.add_argument('--dpi', type=int, default=300,
                  help='Dots-per-inch (DPI) for the output. '
                       'Default is: "%(default)s"')  

    #venn
    venn_parser = subparsers.add_parser('venn', usage='intervene venn [options]', 
        description='Create Venn diagram upto 6-way after intersection of genomic regions in <BED/GTF/GFF/VCF> or list sets.', 
        help='Venn diagram of intersection of genomic regions or list sets (upto 6-way).')
    venn_parser.add_argument('-a', dest="a", required=True, default=None, help='BED or list of genes/names file 1 (required)')
    venn_parser.add_argument('-b', dest="b", required=True, default=None, help='BED or list of genes/names file 2 (required)')
    venn_parser.add_argument('-c', dest="c", default=None, help='BED or list of genes/names file 3 (optional)')
    venn_parser.add_argument('-d', dest="d", default=None, help='BED or list of genes/names file 4 (optional)')
    venn_parser.add_argument('-e', dest="e", default=None, help='BED or list of genes/names file 5 (optional)')
    venn_parser.add_argument('-f', dest="f", default=None, help='BED or list of genes/names file 6 (optional)')
    
    venn_parser.add_argument('--type', dest='type', choices=('genomic','list'),
                  help='Type of input sets. Genomic regions or lists of genes sets. ')
   
    venn_parser.add_argument('--labels', dest='labels', default='A,B,C,D,E,F',
                  help='Comma-separated list of names for input files. '
                       'Default is: --labels=A,B,C,D,E,F')
   
    venn_parser.add_argument('--colors', dest='colors',
                  help='Comma-separated list of matplotlib-valid colors. '
                       'E.g., --colors=r,b,k')
    
    venn_parser.add_argument('-o', '--output', dest='output', 
                  help='Output folder path where plots will store.'
                       'Default is current working directory.')
    venn_parser.add_argument('--figtype', dest="figtype",choices=('pdf','svg','png','tif','jpg'), 
                   default='pdf',help='Figure type for the plot. '
                       'e.g. --figtype svg. Default is "%(default)s"')    
    venn_parser.add_argument('--figsize', default=(8,10),
                   help='Figure size for the output plot. '
                       'e.g. --figsize=8,10 Default is "%(default)s"')    
    venn_parser.add_argument('--dpi', type=int, default=300,
                  help='Dots-per-inch (DPI) for the output. '
                       'Default is: "%(default)s"')  
    venn_parser.add_argument('--fill', choices=('number','percentage'),default='number',
                  help='Report number or  percentage of overlaps (Only if --type=list)'
                       'Default is "%(default)s"')

    #upset
    upset_parser = subparsers.add_parser('upset', usage='intervene upset [options]', 
        description='Create UpSet diagram after intersection of genomic regions in <BED/GTF/GFF/VCF> or list sets.', 
        help='UpSet diagram of intersection of genomic regions or list sets.')

    upset_parser.add_argument('-a', dest="a", required=True, default=None, help='BED or list of genes/names file 1 (required)')
    upset_parser.add_argument('-b', dest="b", required=True, default=None, help='BED or list of genes/names file 2 (required)')
    upset_parser.add_argument('-c', dest="c", default=None, help='BED or list of genes/names file 3 (optional)')
    upset_parser.add_argument('-d', dest="d", default=None, help='BED or list of genes/names file 4 (optional)')
    upset_parser.add_argument('-e', dest="e", default=None, help='BED or list of genes/names file 5 (optional)')
    upset_parser.add_argument('-f', dest="f", default=None, help='BED or list of genes/names file 6 (optional)')
    
    upset_parser.add_argument('--type', dest='type', choices=('genomic','list'),default='genomic',
                  help='Type of input sets. Genomic regions or lists of genes sets. '
                       'Default is "%(default)s"') 
   
    upset_parser.add_argument('--labels', dest='labels', default='A,B,C,D,E,F',
                  help='Comma-separated list of names for input files. '
                       'Default is: --labels=A,B,C,D,E,F')
   
    upset_parser.add_argument('--colors', dest='colors',
                  help='Comma-separated list of matplotlib-valid colors. '
                       'E.g., --colors=r,b,k')

    upset_parser.add_argument('-o', '--output', dest='output', 
                  help='Output folder path where plots will store.'
                       'Default is current working directory.')
    upset_parser.add_argument('--order', dest="order",choices=("freq", "degree"), 
                   default='freq',help='The order of intersections of sets. '
                       'e.g. --order degree. Default is "%(default)s"')

    upset_parser.add_argument('--mbcolor', type=str, default='brown', 
                  help='Color of the main bar plot.'
                       'Default is: "%(default)s"')
    upset_parser.add_argument('--sbcolor', type=str, default='blue', 
                  help='Color of set size bar plot.'
                       'Default is: "%(default)s"')

    upset_parser.add_argument('--mblabel', type=str, default='No of Intersections', 
                  help='The y-axis label of the intersection size bars.'
                       'Default is: "%(default)s"')
    upset_parser.add_argument('--sxlabel', type=str, default='Set size', 
                  help='The x-axis label of the set size bars.'
                       'Default is: "%(default)s"')
           
    upset_parser.add_argument('--figtype', dest="figtype",choices=('pdf','svg','png'), 
                   default='pdf',help='Figure type for the plot. '
                       'e.g. --figtype svg. Default is "%(default)s"')    
    upset_parser.add_argument('--figsize', default=(8,10),
                   help='Figure size for the output plot. '
                       'e.g. --figsize=8,10 Default is "%(default)s"')    
    upset_parser.add_argument('--dpi', type=int, dest='dpi', default=300,
                  help='Dots-per-inch (DPI) for the output. '
                       'Default is: "%(default)s"')
    
    parser.add_argument('--test', action='store_true', help='This will run the program on test data.')
    
    parser.add_argument('-v','--version', dest='version', action='version', version='%(prog)s 1.0')

    options = parser.parse_args()

    if options.test:
        pybedtools.bedtool.random.seed(1)
        a = example_bedtool('rmsk.hg18.chr21.small.bed')
        b = example_bedtool('venn.b.bed')
        c = example_bedtool('venn.c.bed')
        options.a = a.fn
        options.b = b.fn
        options.c = c.fn
        #options.colors='r,b,g'
        options.output = 'bedVenn.png'
        options.labels = ['A','B','C']
        sys.exit(1)

    if not options.command:
        venn_parser.print_help()
        sys.stderr.write('Missing required arguments. ')
        sys.exit(1) 

    #making the out folder if it doesn't exist
    if options.output:
        output_dir = create_dir(options.output)
    else:
        options.output = create_dir(os.getcwd()+"/InterVene_results")

    if options.command =='pairwise':
        print("\nPerforming a pairwise intersection/overlap analysis.\n")
        pairwise.pairwise_intersection(options)
        sys.exit(1)

    output_name =  options.output+'/InterVene_'+options.command+'_'+str(venn_ways(options))+'way_'+options.type+'.'+options.figtype

    #checke if there are atleast two (a & b) bed/list files    
    reqd_args = ['a','b']
    if not options.test:
        for ra in reqd_args:
            if not getattr(options,ra):
                if options.command == 'venn':
                    venn_parser.print_help()
                else:
                    upset_parser.print_help()
                sys.stderr.write('Missing required arg "%s"\n' % ra)
                sys.exit(1)

    if options.command == 'venn' or options.command == 'upset':
        if not options.type:
            if options.command == 'venn':
                venn_parser.print_help()
            else:
                upset_parser.print_help()
            sys.stderr.write('Missing required arg --type {genomic,list}')
            sys.exit(0)
    
    if options.command == 'upset':
        plot_type = 'upset'
    else:
        plot_type = 'venn'

    if venn_ways(options) == 2:
        print('\nGenerating a 2-way "%s" diagram.\n' %options.command)
        if options.labels:
            label_names = options.labels.split(',')
        else:
            label_names = ['A','B']

        #If the input is a gene list
        if options.type == 'list':
            #print options.a[0]
            a = open(options.a, 'r').readlines()
            b = open(options.b, 'r').readlines()

            labels = list_venn.get_labels([a,b], fill=[str(options.fill)])
            fig, ax = list_venn.venn2(labels, names=label_names)
            
        #else input considered as bed file
        else:
            fig, ax = genomic_venn.venn2(a=options.a, b=options.b, names=label_names, plot_type=plot_type, dpi=options.dpi, output=options.output, fig_type=options.figtype)
     
    elif venn_ways(options) == 3:
        print('\nGenerating a 3-way "%s" diagram.\n' %options.command)
        if options.labels:
            label_names = options.labels.split(',')
        else:
            label_names = ['A','B','C']
        #If the input is a gene list
        if options.type == 'list':
            a = open(options.a, 'r').readlines()
            b = open(options.b, 'r').readlines()
            c = open(options.c, 'r').readlines()
            labels = list_venn.get_labels([a, b, c], fill=[str(options.fill)])
            fig, ax = list_venn.venn3(labels, names=label_names)
            
        #else input considered as bed file
        else:
            fig, ax = genomic_venn.venn3(a=options.a, b=options.b, c=options.c, 
                names=label_names, plot_type=plot_type, dpi=options.dpi, output=options.output, fig_type=options.figtype)

    elif venn_ways(options) == 4:
        print('\nGenerating a 4-way "%s" diagram.\n' %options.command)
        if options.labels:
            label_names = options.labels.split(',')
        else:
            label_names = ['A','B','C','D']
        #If the input is a gene list
        if options.type == 'list':

            if options.command == 'upset':
                cmd = 'intervene_upset_plot.R %s %s %s %s %s %s %s %s' % ('list',4,options.a,options.b,options.c,options.d, options.o, options.labels)
                os.system(cmd)
                sys.exit(1)

            else:
                a = open(options.a, 'r').readlines()
                b = open(options.b, 'r').readlines()
                c = open(options.c, 'r').readlines()
                d = open(options.d, 'r').readlines()
                labels = list_venn.get_labels([a, b, c, d], fill=[str(options.fill)])
                fig, ax = list_venn.venn4(labels, names=label_names)
            
        #else input considered as bed file
        else:
             fig, ax = genomic_venn.venn4(a=options.a, b=options.b, c=options.c, d=options.d, 
                names=label_names, plot_type=plot_type, dpi=options.dpi, output=options.output, fig_type=options.figtype)
            
                   
    elif venn_ways(options) == 5:
        print('\nGenerating a 5-way "%s" diagram.\n' %options.command)
        if options.labels:
            label_names = options.labels.split(',')
        else:
            label_names = ['A','B','C','D','E']
        #If the input is a gene list
        if options.type == 'list':

            if options.command == 'upset':
                cmd = 'intervene_upset_plot.R %s %s %s %s %s %s %s %s %s' % ('list',5,options.a,options.b,options.c,options.d, options.e,options.o, options.labels)
                os.system(cmd)
                sys.exit(1)
            else: 
                a = open(options.a, 'r').readlines()
                b = open(options.b, 'r').readlines()
                c = open(options.c, 'r').readlines()
                d = open(options.d, 'r').readlines()
                e = open(options.e, 'r').readlines()

                labels = list_venn.get_labels([a, b, c, d, e], fill=[str(options.fill)])
                fig, ax = list_venn.venn5(labels, names=label_names)
            
        #else input considered as genomic regions file
        else:
            fig, ax = genomic_venn.venn5(a=options.a, b=options.b, c=options.c, d=options.d, e=options.e, 
                names=label_names, plot_type=plot_type, dpi=options.dpi, output=options.output, fig_type=options.figtype)
        
    elif venn_ways(options) == 6:
        print('\nGenerating a 6-way "%s" diagram.\n' %options.command)
        if options.labels:
            label_names = options.labels.split(',')
        else:
            label_names = ['A','B','C','D','E','F']
        #If the input is a gene list
        if options.type == 'list':
            if options.ptype == 'upset':
                cmd = 'intervene_upset_plot.R %s %s %s %s %s %s %s %s %s %s' % ('list',6,options.a,options.b,options.c,options.d, options.e, options.f,options.o, options.labels)
                os.system(cmd)
                sys.exit(1)
            else:
                a = open(options.a, 'r').readlines()
                b = open(options.b, 'r').readlines()
                c = open(options.c, 'r').readlines()
                d = open(options.d, 'r').readlines()
                e = open(options.e, 'r').readlines()
                f = open(options.f, 'r').readlines()

                labels = list_venn.get_labels([a, b, c, d, e, f], fill=[str(options.fill)])
                fig, ax = list_venn.venn6(labels, names=label_names)
                
        #else input considered as bed file
        else:
            fig, ax = genomic_venn.venn6(a=options.a, b=options.b, c=options.c, d=options.d, e=options.e, f=options.f, 
                names=label_names, plot_type=plot_type, dpi=options.dpi, output=options.output, fig_type=options.figtype)
    else:
        parser.print_help()
        sys.stderr.write('Please make sure your arguments are correct.')
        sys.exit(1)

    fig.savefig(output_name, dpi=options.dpi, bbox_inches='tight')
    plt.close()
    print('\nYou are done! Please check your results @ '+options.output+'. \nThank you for using InterVene!\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("I got interrupted. :-( Bye!\n")
        sys.exit(0)
