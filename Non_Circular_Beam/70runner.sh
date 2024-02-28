#!/bin/bash

# Specify the file name
filename="files_070.txt"

# Read the contents of the file
num=-1
while IFS= read -r line
do
  # Download the file
  wget -c "$line"
  num=$((num+1))
  

  if [ $num -lt 10 ]; then
    current_name="product-action?SIMULATED_MAP.FILE_ID=febecop_ffp10_lensed_scl_cmb_070_mc_000$num.fits"
    New_name="galactic_cmb_070_mc_000${num}_1.fits"
    mv "$current_name" "$New_name"
    cd /home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/input/
    string1="\"_cmb_070_mc_000${num}_\""
    string2=" 			  	       --> Suffix1"
    new_content="${string1}"${string2}
    echo $new_content
    lne_number=2
    filename2="iso"
    sed -i "${lne_number} s/.*/${new_content}/" "$filename2"
    cd ../
    ./nrun
    cd f070/
    mkdir ${num}
    cd ${num}
    source1="/home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/OUTPUT/testout/HS/ALMS/galactic/"
    #source2="/home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/OUTPUT/testout/HS/ALMS/galactic/AL2M0D2.dat"
    mv  "$source1"/* .
    #mv "$source2" .
    cd ../../Data/


  fi
  if [ $num -lt 100 ] && [ $num -ge 9 ]; then
    current_name="product-action?SIMULATED_MAP.FILE_ID=febecop_ffp10_lensed_scl_cmb_070_mc_00$num.fits"
    New_name="galactic_cmb_070_mc_00${num}_1.fits"
    mv "$current_name" "$New_name"
    cd /home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/input/
    string1="\"_cmb_070_mc_00${num}_\""
    string2=" 			  	       --> Suffix1"
    new_content="${string1}"${string2}
    echo $new_content
    lne_number=2
    filename2="iso"
    sed -i "${lne_number} s/.*/${new_content}/" "$filename2"
    cd ../
    ./nrun
    cd f070/
    mkdir ${num}
    cd ${num}
    source1="/home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/OUTPUT/testout/HS/ALMS/galactic/"
    #source2="/home/akashdeep/Downloads/BipoSH_code-20230821T064006Z-001/BipoSH_code/OUTPUT/testout/HS/ALMS/galactic/AL2M0D2.dat"
    mv  "$source1"/* .
    cd ../../Data/

  fi

done < "$filename"