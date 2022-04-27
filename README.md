# closeness_by_component
This script is related to this publication: https://www.biorxiv.org/content/10.1101/2022.04.19.488343v1<br/>
It will process a file or a folder, and will calculate the combined closeness for a graph and all subgraphs in this graph.
Technically it solely utilizes the closeness function (with parameter wf_improved=False) in Networkx, without any mathematical changes. This script simply exposes the functions for a non-programming end-user to use for data analysis.

## Requirements
This tool is written in Python3.<br/>
It requires networkx https://networkx.org/ .<br/>
It also requires networkxgmml https://pypi.org/project/networkxgmml/, which is the standard output by EFI-EST https://efi.igb.illinois.edu/efi-est/ .<br/>


## How to use
Simply call either:<br/>
python3 get_metrics_closeness_by_component.py --input_file /home/exampleuser/exampleinput.gml <br/>
OR<br/>
python3 get_metrics_closeness_by_component.py --input_file /home/exampleuser/exampleinput.xgmml<br/>
OR<br/>
python3 get_metrics_closeness_by_component.py --input_folder /home/exampleuser/examplefolder<br/>
<br/>
You may give an output name in case you use --input_file, with --output_file . If no output name is given, the output file will be named input file + .closeness.csv . In case a whole folder is processed, all output file names will be generated like this.

Please note:
If the input file contains only one network, you will still get 2 lines in the output: Once for the whole network, and once for the first (and only) subnetwork.

## Citation
Please cite https://www.biorxiv.org/content/10.1101/2022.04.19.488343v1 (as well as Networkx) in case you use this script.<br/>

## License
This software is distributed under the GPLv3.<br/>
