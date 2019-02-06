Given the virtual slide images of CD3 and CD8 immunohistochemical stains, this protocol provides the following quantitative measures of tumor immune microenvironment:

- Density of intraepithelial/stromal tumor-infiltrating lymphocytes (TIL)
- Proportion of stroma within an annotated tumor area
- Ratio of intraepithelial and stromal TIL 
- Ratio of CD8 and CD3 TIL 

Once you annotate the tumor area manually, it segments the area into 1000 x 1000-pixel tiles. This enables you to assess not only the overall density of TIL and stroma, but also their mean, minimum, median, maximum and variance over the tiles. 


#[Thing to prepare]
##1. Computer (of course)
 This protocol has been tested on the machines with the following specification: 
Windows 10, AMD Ryzen 7 1700 3.00 GHz (RAM 32GB)
Windows 7, Intel i7-4790 3.60 GHz (RAM 32GB)
Ubuntu 14.04 LTS, Intel Xeon 3.40 GHz (RAM 32GB) 

To summerize, no supercomputer needed. I have to nothing to say about Mac machines since I have never used them. 


##2. Software 
- Python 2.7 (NOT 3.X) 
- R 
- QuPath (https://qupath.github.io/)

 It seems that the availability of a machine totally depends on the operability of QuPath; I discovered that QuPath is not as stable on Linux as it is on Windows. In fact, I failed to run this algorithm on a centOS linux 7 supercomputer. It would be helpful to check the googlegroup of QuPath users (Link) when you have troubles with QuPath. 
 As a window user, I used Anaconda (https://www.anaconda.com/download/) because I needed numpy.. you might try other options here (https://scipy.org/install.html) 


##3. Your own virtual slides 
 For each patient case, a representative tumor block was selected, immunohistochemistry of CD3 and CD8 was performed and the slides were scanned by Aperio AT2 slide scanner at 20x magnification. Why not 40x? just storage issues. I've also tried some images scanned at 40x manification but had no problem. 
 
 
