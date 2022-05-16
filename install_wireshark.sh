#!/bin/sh
# This shell script was originally made by SyneArt <sa@syneart.com>
#######################################
# BUILD WIRESHARK ON UBUNTU OR DEBIAN #
#######################################

# 1. KEEP UBUNTU OR DEBIAN UP TO DATE
sudo apt-get -y update

# 2. INSTALL THE DEPENDENCIES
sudo apt-get install -y build-essential git cmake 

# CMAKE3
sudo apt-get install -y cmake3

# GUI
sudo apt-get install -y qttools5-dev qttools5-dev-tools libqt5svg5-dev qtmultimedia5-dev

# PCAP
sudo apt-get install -y libpcap-dev

# Dev file (On Ubuntu 20.04)
sudo apt-get install -y libc-ares-dev

# CRYPT
sudo apt-get install -y libgcrypt20-dev

# GLIB2
sudo apt-get install -y libglib2.0-dev

# LEX & YACC
sudo apt-get install -y flex bison

# PCRE2 (On Ubuntu 18.04)
sudo apt-get install -y libpcre2-dev

# HTTP/2 protocol (Ubuntu >= 16.04)
sudo apt-get install -y libnghttp2-dev

# 3. BUILD THE WIRESHARK
git clone https://github.com/wireshark/wireshark ~/wireshark
cd ~/wireshark
mkdir build
cd build
cmake ../
make -j`nproc` && {
  echo "\nBuild Success!"
  echo "You can execute the Wireshark by command \"sudo ./wireshark\""
  echo "at \"`pwd`/run\""
}

# You can execute the Wireshark by command "sudo ./wireshark"
at "/home/abreu/wireshark/build/run"
