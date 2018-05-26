# fm-index-search
## Description  
Efficient string search that employs Burrows-Wheeler Transformation and FM-Index  

## Running  
Run fmindex.py with following arguments:  
  **-t** or **--text**      *path to the text file containing input string*  
  **-p** or **--patterns**  *path to the text file containing search patterns (each pattern in new line)*  
  **-r** or **--results**   *optional argument. specifies path to the output file*  
  
Run fmindex_optimized.py with following arguments:  
  **-t** or **--text**      *path to the text file containing input string*  
  **-p** or **--patterns**  *path to the text file containing search patterns (each pattern in new line)*  
  **-r** or **--results**   *optional argument. specifies path to the output file*  
  **--sa_factor**   *optional argument. defines suffix array degree of compression*  
  **--tally_factor**   *optional argument. defines tally matrix degree of compression*  
  
You can find sample files in **data** directory

## Presentation
Presentation can be found on
https://docs.google.com/presentation/d/1I7S8K_UeHsi7_kbph-koO5cQ94C4KhDzTMktHblMorQ/edit?usp=sharing
