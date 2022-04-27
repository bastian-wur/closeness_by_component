# -*- coding: utf-8 -*-
"""
Created on Wed April 27
@author: Bastian Hornung
email bastian dot hornung at gmx dot germany-tld
Written in Python3
This script takes a network file (.gml or .xgmml), or a folder with such files
and calculates for each of them the closeness for each network and subnetwork

Requires: https://pypi.org/project/networkxgmml/
Tested with version 0.1.6 from October 2015.
Requires: Networkx
"""

import networkx as nx
import os
import sys
import argparse
import networkxgmml

def calc_value_dic(curDic):
    """function takes a dictionary, iterates it
    sums up the values and calcuales the aveage
    """
    fSum = 0
    for key,value in curDic.items():
        fSum = fSum+float(value)
    fAv = fSum/len(curDic)
    return fAv

def calculate_properties(G,sFile,i,outputFile):
    """Gets all the properties from the current (sub)graph and writes them to the output file.
    This includes the number of components, nodes, edges, and finally the closeness.
    wf_improved needs to be set to false. See https://www.biorxiv.org/content/10.1101/2022.04.19.488343v1
    """
    
    if i==-1:
        sSubNetwork="whole_network"
    else:
        sSubNetwork = "subnetwork_"+str(i)    
    iComp = nx.number_connected_components(G)
    iNodes = len(nx.nodes(G))
    iEdge  = G.number_of_edges()    
    dicCloseness = nx.closeness_centrality(G,wf_improved=False)
    fCloseness = calc_value_dic(dicCloseness)
    outputFile.write(sFile+"\t"+sSubNetwork+"\t"+str(iComp)+"\t"+str(iNodes)+"\t"+str(iEdge)+"\t"+str(fCloseness)+"\n")

def get_graph(sFile):
    """Loads the graph from a gml or xgmml file
    """
    
    if sFile.endswith("gml"):
        G = nx.read_gml(sFile)
    elif sFile.endswith("xgmml"):
        handle = open(sFile,"rb")
        G =  networkxgmml.XGMMLReader(handle)
        handle.close()
    else:
        print ("file does not end with .gml or .xgmml, exiting!")
        sys.exit()
    return G

def process_graph(sFile,sOut):
    """Gets the graph, makes it undirected, then calculates the necessary values for
    the whole graph, then iterates over subgraphs and performs the same calculations.
    """
    
    print ("processing: "+sFile)
    G =  get_graph(sFile)
    G = G.to_undirected()
    outputFile = open(sOut,"w")
    outputFile.write("file\tnumber of subnetwork\tnumber_subnetworks\tnumber_nodes\tnumber_edges\taverage_closeness\n")    
    cComp = nx.connected_components(G)
    calculate_properties(G,sFile,-1,outputFile)
    for i,item in enumerate(cComp):
        GNewSub = G.subgraph(item)#.copy() #copy only necessary if there are changes in the graph to be made                  
        calculate_properties(GNewSub,sFile,i,outputFile)
    outputFile.close()
    print ("finished processing: "+sFile)
    print ("output written to: "+sOut,"\n")

def process_single_file(sFile,sOut):
    if not os.path.isfile(sFile):
        print (sFile+" does not exist, exiting!")
        sys.exit()   
    if not sOut:
        sOut = sFile+".closeness.csv"
    process_graph(sFile,sOut)

def process_folder(sFolder):
    """processes all gml or xgmml files in a folder
    Will warn if no valid files are found
    """
    
    if not os.path.isdir(sFolder):
        print (sFolder+" is not a valid folder, exiting!")
        sys.exit()         
    lFiles = os.listdir(sFolder)
    bFoundFile = False
    for files in lFiles:
        if files.endswith(".gml") or files.endswith("xgmml"):
            sOut = sFolder+files+".closeness.csv"
            process_graph(sFolder+files,sOut)
            bFoundFile = True
    if not bFoundFile:
        print ("no valid files ending with .gml or .xgmml could be found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()   
    parser.add_argument("--input_file",type=str,help="input network as either gml or xgmml")
    parser.add_argument("--input_folder",type=str,help="will process all gml or xgmml files in a folder")    
    parser.add_argument("--output_file",type=str,help="output file name. Default: input file plus .closeness.csv")

    args = parser.parse_args()
    sFile = args.input_file
    sFolder = args.input_folder
    sOut = args.output_file
    if sFile:
        process_single_file(sFile,sOut)
    elif sFolder:
        process_folder(sFolder)
    else:
        print ("you need to provide at minimum an input file via --input_file or input folder via --input_folder")
        parser.print_help()
        sys.exit()


