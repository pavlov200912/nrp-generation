# NRP Generation
<a name="sec_run_quick"></a>
## Quick start

**Download** [test data](https://github.com/ablab/nerpa/releases/download/v1.0.0/test_data.tar.gz):

    wget https://github.com/ablab/nerpa/releases/download/v1.0.0/test_data.tar.gz
    tar xzf test_data.tar.gz

**Example**: five BGCs sequences downloaded from [MIBiG](https://mibig.secondarymetabolites.org/) and pre-processed with antiSMASH v.3 against five NRPs in the SMILES format (provided a single database tab-separated file)

Run nerpa 

	nerpa.py -a test_data/MIBiG_subset/genome_predictions --smiles-tsv test_data/MIBiG_subset/structures_info.tsv
  
Run NRP Generation 

	python3 main.py --output="./out_detect" --algorithm=replacements ./nerpa_results/latest/ 
  
 

**Check out suggested graphs**:  
    
    cat ./out_detect/compound_000002_BGC0000447.txt

**Output format**:

For each NRP and BGC alignment graph variants scored in:

  `{output}/compound_{compound number as in the nerpa files}_BGC{bgc number}.txt` 

In this file graph variants are separated with \n and stored in this format: 

  `(vertex_name,)+;(vertex_index1, vertex_index2,monomer_bond_name;)+` 
  
 For example:
 
  `aThr/Thr,Dab,Leu,Gln;0,1,AMINO;2,3,AMINO;`
 
